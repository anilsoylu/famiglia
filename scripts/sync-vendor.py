#!/usr/bin/env python3
"""Copy third-party skills listed in vendor.json into skills/, pinned to a commit.

  scripts/sync-vendor.py          fetch each repo at its ref, replace skills/<name>, write vendor.lock.json
  scripts/sync-vendor.py --check  fetch and compare only; exit 1 if any bundled skill drifted from its pinned source
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {".DS_Store", ".git"}


def tree_hash(path: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(p for p in path.rglob("*") if p.is_file() and not SKIP & set(p.parts)):
        h.update(str(f.relative_to(path)).encode() + b"\0" + f.read_bytes() + b"\0")
    return h.hexdigest()


def fetch(repo: str, ref: str, dest: Path) -> None:
    run = lambda *a: subprocess.run(["git", "-C", str(dest), *a], check=True, capture_output=True)
    dest.mkdir(parents=True)
    run("init", "-q")
    run("remote", "add", "origin", repo)
    run("fetch", "-q", "--depth", "1", "origin", ref)
    run("checkout", "-q", "FETCH_HEAD")


def main() -> int:
    check = "--check" in sys.argv
    cfg = json.loads((ROOT / "vendor.json").read_text())
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
            for name_, rel in src["skills"].items():
                upstream, local = repo_dir / rel, ROOT / "skills" / name_
                want = tree_hash(upstream)
                have = tree_hash(local) if local.exists() else None
                if check:
                    status = "ok" if want == have else ("missing" if have is None else "DRIFT")
                    if status != "ok":
                        drift.append(name_)
                    print(f"{status:8} {name_:16} {src['repo']}@{src['ref'][:7]}")
                    continue
                # stage next to the target, then swap, so an interrupted run never leaves a half-copied skill
                staging = local.with_name(f".{name_}.staging")
                shutil.rmtree(staging, ignore_errors=True)
                shutil.copytree(upstream, staging, ignore=shutil.ignore_patterns(*SKIP))
                shutil.rmtree(local, ignore_errors=True)
                staging.rename(local)
                lock[name_] = {"repo": src["repo"], "ref": src["ref"], "path": rel, "license": src["license"], "sha256": want}
                print(f"synced   {name_:16} {src['repo']}@{src['ref'][:7]}")
            if not check:
                lic_dir = ROOT / "LICENSES" / name
                lic_dir.mkdir(parents=True, exist_ok=True)
                for lf in src["license_files"]:
                    shutil.copy2(repo_dir / lf, lic_dir / lf)
    if check:
        print("no drift" if not drift else f"drift: {', '.join(drift)}")
        return 1 if drift else 0
    (ROOT / "vendor.lock.json").write_text(json.dumps(lock, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
