#!/usr/bin/env python3
"""Audit GitHub Actions run times: waiting, setup and running per job, at p50 and p95.

Pulls the last N completed runs through `gh api` and prints a markdown report:
- per job: waiting (job created until a runner starts it; this includes waiting on `needs` jobs), setup (checkout, toolchain, cache, install, post steps),
  running (everything else), and total, each at p50 and p95;
- PR result time: first run created to last job completed, per head commit, at p50 and p95;
- CI minutes per month, scaled from the audit window (each job rounded up to a whole minute, as GitHub bills).

Usage: python3 ci-audit.py [--repo owner/name] [--runs 150] [--event pull_request] [--workflow ci.yml] [--json]
"""
import argparse, json, math, re, subprocess, sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

SETUP = (r"^(set up job|complete job|post |initialize containers|stop containers|checkout|run actions/checkout"
         r"|set ?up |run actions/setup-|run .*/setup-|cache|restore|run actions/cache|install|run (bun|npm|pnpm|yarn)"
         r" (install|ci)|download artifact)")


def gh(path: str):
    for _ in range(3):  # network blips only; the audit itself never hides a failure
        out = subprocess.run(["gh", "api", path], capture_output=True, text=True)
        if not out.returncode:
            return json.loads(out.stdout)
    sys.exit(f"gh api {path} failed: {out.stderr.strip()}")


def ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def secs(start, end):
    return (ts(end) - ts(start)).total_seconds() if start and end else None


def pct(values, p):
    if not values:
        return None
    ordered = sorted(values)
    return ordered[max(0, math.ceil(p / 100 * len(ordered)) - 1)]


def fmt(value):
    if value is None:
        return "-"
    return f"{value:.0f}s" if value < 120 else f"{value / 60:.1f}m"


def runs(repo, n, event, workflow):
    base = f"repos/{repo}/actions/workflows/{workflow}/runs" if workflow else f"repos/{repo}/actions/runs"
    found, page = [], 1
    while len(found) < n:
        batch = gh(f"{base}?status=completed&per_page=100&page={page}" + (f"&event={event}" if event else ""))
        found += batch.get("workflow_runs", [])
        if len(batch.get("workflow_runs", [])) < 100:
            break
        page += 1
    return found[:n]


def jobs(repo, run_id):
    return gh(f"repos/{repo}/actions/runs/{run_id}/jobs?per_page=100").get("jobs", [])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", help="owner/name (default: the current repo)")
    ap.add_argument("--runs", type=int, default=150)
    ap.add_argument("--event", default="pull_request", help="run event filter; '' for all events")
    ap.add_argument("--workflow", help="workflow file name or id, e.g. ci.yml")
    ap.add_argument("--setup-pattern", default=SETUP, help="regex (case-insensitive) for setup step names")
    ap.add_argument("--json", action="store_true", help="print raw per-job numbers as JSON")
    args = ap.parse_args()

    repo = args.repo or subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
                                       capture_output=True, text=True).stdout.strip()
    if not repo:
        sys.exit("No repo: pass --repo owner/name, or run inside a clone with a GitHub remote and `gh auth login` done.")
    setup_re = re.compile(args.setup_pattern, re.I)

    run_list = runs(repo, args.runs, args.event, args.workflow)
    if not run_list:
        sys.exit(f"No completed runs for {repo} (event={args.event or 'any'}). There is no history to audit.")
    with ThreadPoolExecutor(8) as pool:
        job_lists = list(pool.map(lambda r: jobs(repo, r["id"]), run_list))

    per_job = defaultdict(lambda: defaultdict(list))
    commits = defaultdict(lambda: [None, None])
    billed = 0
    for run, job_list in zip(run_list, job_lists):
        for job in job_list:
            total = secs(job.get("started_at"), job.get("completed_at"))
            if not total or total <= 0 or job.get("conclusion") == "skipped":
                continue
            setup = sum(secs(s.get("started_at"), s.get("completed_at")) or 0
                        for s in job.get("steps", []) if setup_re.search(s["name"]))
            key = f"{run['name']} / {job['name']}"
            numbers = per_job[key]
            numbers["waiting"].append(max(0.0, secs(job.get("created_at") or run["created_at"], job["started_at"])))
            numbers["setup"].append(min(setup, total))
            numbers["running"].append(max(0.0, total - setup))
            numbers["total"].append(numbers["waiting"][-1] + total)
            billed += math.ceil(total / 60)
            first, last = commits[run["head_sha"]]
            commits[run["head_sha"]] = [min(filter(None, [first, ts(run["created_at"])])),
                                        max(filter(None, [last, ts(job["completed_at"])]))]

    if args.json:
        print(json.dumps({k: dict(v) for k, v in per_job.items()}, indent=2))
        return

    created = [ts(r["created_at"]) for r in run_list]
    days = max((max(created) - min(created)).total_seconds() / 86400, 1)
    results = [(last - first).total_seconds() for first, last in commits.values() if first and last]

    print(f"# CI audit: {repo}\n")
    print(f"{len(run_list)} runs (event={args.event or 'any'}), {min(created):%Y-%m-%d} to {max(created):%Y-%m-%d}, "
          f"{len(commits)} commits.\n")
    print(f"PR result time: p50 {fmt(pct(results, 50))}, p95 {fmt(pct(results, 95))}\n")
    print(f"CI minutes: {billed} in {days:.0f} days, about {billed / days * 30:.0f} per month\n")
    print("| job | runs | waiting p50/p95 | setup p50/p95 | running p50/p95 | total p50/p95 |")
    print("|---|---|---|---|---|---|")
    order = sorted(per_job.items(), key=lambda kv: -(pct(kv[1]["total"], 95) or 0))
    for name, n in order:
        cells = " | ".join(f"{fmt(pct(n[b], 50))} / {fmt(pct(n[b], 95))}"
                           for b in ("waiting", "setup", "running", "total"))
        print(f"| {name} | {len(n['total'])} | {cells} |")
    buckets = ("waiting", "setup", "running")
    slow_name, slow = max(per_job.items(), key=lambda kv: pct(kv[1]["total"], 50) or 0)
    slow_b = max(buckets, key=lambda b: pct(slow[b], 50) or 0)
    sums = {b: sum(pct(n[b], 50) or 0 for n in per_job.values()) for b in buckets}
    cost_b = max(sums, key=sums.get)
    print("\nWaiting includes time spent on `needs` jobs: a long wait on a job with `needs` is a shape problem, not a"
          " runner problem.")
    print(f"PR time: the slowest job by p50 is '{slow_name}', and its biggest bucket is {slow_b}"
          f" ({fmt(pct(slow[slow_b], 50))}).")
    print(f"Cost: summed over all jobs, the biggest bucket is {cost_b} ({fmt(sums[cost_b])} per run at p50).")


if __name__ == "__main__":
    main()
