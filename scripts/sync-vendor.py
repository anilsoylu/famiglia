#!/usr/bin/env python3
"""Copy third-party skills listed in vendor.json into skills/, pinned to a commit.

  scripts/sync-vendor.py           fetch each repo at its ref, replace skills/<name>, write vendor.lock.json
  scripts/sync-vendor.py --check   fetch and compare only; exit 1 if any bundled skill drifted from its pinned source
  scripts/sync-vendor.py --latest  bump every ref in vendor.json to the repo's HEAD first (combine with --check to preview)

A skill is a path inside the repo, or {"path": ..., "files": [...]} to copy only those files (for a skill at a repo root).
"""
import hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {".DS_Store", ".git"}


def skill_files(path: Path, files: list | None) -> list[Path]:
    if files:
        return sorted(path / f for f in files)
    return sorted(p for p in path.rglob("*") if p.is_file() and not SKIP & set(p.parts))


def tree_hash(path: Path, files: list | None = None) -> str:
    h = hashlib.sha256()
    for f in skill_files(path, files):
        h.update(str(f.relative_to(path)).encode() + b"\0" + f.read_bytes() + b"\0")
    return h.hexdigest()


def fetch(repo: str, ref: str, dest: Path) -> None:
    run = lambda *a: subprocess.run(["git", "-C", str(dest), *a], check=True, capture_output=True)
    dest.mkdir(parents=True)
    run("init", "-q")
    run("remote", "add", "origin", repo)
    run("fetch", "-q", "--depth", "1", "origin", ref)
    run("checkout", "-q", "FETCH_HEAD")


def head(repo: str) -> str:
    out = subprocess.run(["git", "ls-remote", repo, "HEAD"], check=True, capture_output=True, text=True).stdout
    return out.split()[0]


def main() -> int:
    check, latest = "--check" in sys.argv, "--latest" in sys.argv
    cfg = json.loads((ROOT / "vendor.json").read_text())
    if latest:
        for src in cfg["sources"]:
            new = head(src["repo"])
            if new != src["ref"]:
                print(f"bump     {src['repo']} {src['ref'][:7]} -> {new[:7]}")
                src["ref"] = new
    lock, drift = {}, []
    with tempfile.TemporaryDirectory() as tmp:
        for i, src in enumerate(cfg["sources"]):
            repo_dir = Path(tmp) / str(i)
            try:
                fetch(src["repo"], src["ref"], repo_dir)
            except subprocess.CalledProcessError as e:
                print(f"FAIL fetch {src['repo']}@{src['ref'][:7]}: {e.stderr.decode().strip()}", file=sys.stderr)
                return 2
            name = src["repo"].rstrip("/").split("/")[-1]
            for name_, spec in src["skills"].items():
                rel, files = (spec, None) if isinstance(spec, str) else (spec["path"], spec.get("files"))
                upstream, local = repo_dir / rel, ROOT / "skills" / name_
                want = tree_hash(upstream, files)
                have = tree_hash(local) if local.exists() else None
                if check:
                    status = "ok" if want == have else ("missing" if have is None else "DRIFT")
                    if status != "ok":
                        drift.append(name_)
                    print(f"{status:8} {name_:28} {src['repo']}@{src['ref'][:7]}")
                    continue
                # stage next to the target, then swap, so an interrupted run never leaves a half-copied skill
                staging = local.with_name(f".{name_}.staging")
                shutil.rmtree(staging, ignore_errors=True)
                if files:
                    for f in files:
                        (staging / f).parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(upstream / f, staging / f)
                else:
                    shutil.copytree(upstream, staging, ignore=shutil.ignore_patterns(*SKIP))
                shutil.rmtree(local, ignore_errors=True)
                staging.rename(local)
                lock[name_] = {"repo": src["repo"], "ref": src["ref"], "path": rel, "license": src["license"], "sha256": want}
                if files:
                    lock[name_]["files"] = files
                print(f"synced   {name_:28} {src['repo']}@{src['ref'][:7]}")
            if not check:
                lic_dir = ROOT / "LICENSES" / name
                lic_dir.mkdir(parents=True, exist_ok=True)
                # Apache-2.0 §4(d): a NOTICE file travels with the code
                for lf in [*src["license_files"], *(p.name for p in repo_dir.glob("NOTICE*"))]:
                    shutil.copy2(repo_dir / lf, lic_dir / Path(lf).name)
    if check:
        print("no drift" if not drift else f"drift: {', '.join(drift)}")
        return 1 if drift else 0
    if latest:
        (ROOT / "vendor.json").write_text(json.dumps(cfg, indent=2) + "\n")
    (ROOT / "vendor.lock.json").write_text(json.dumps(lock, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
