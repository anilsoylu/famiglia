---
name: cpr
description: >-
  Clean the diff, then open or refresh the PR/MR, and merge it when asked. Ends with the PR link. For "clean and
  PR", "tidy it up and push the PR".
---

# CPR (clean → PR)

`clean` then `pr-update`, in that order, without asking between them. Use it
when the work is done and the branch should end up as a PR someone can read.

Run the two skills for real — this file is the sequence, not a replacement for
their contents.

## Steps

1. **Clean** (`clean`). Re-read the diff, cut dead code and debug logging,
   extend existing helpers instead of paralleling them, match neighboring
   style. Polish only — this is not a test/tsc/lint run.
2. **Shape + publish** (`pr-update`). Topical commits, title and body that
   describe the change as a whole, media in an existing body preserved
   verbatim.
3. **Merge, when the user asked for it** in this request ("merge to main/master",
   "master'a merge et"). Wait for checks (`gh pr checks --watch`), merge with
   the repo's usual method, then check out the default branch and pull so the
   local copy has the merge. A red check stops here, with the failing check
   named.
4. Run any later step the user asked for that the repo documents (a deploy
   script, a release command) yourself, and verify its result before saying
   it's done. Hand back only what needs the user's device, account or decision.
5. End with the PR/MR as a markdown link — number **and** full forge URL.

## Order matters

Clean first, always. Committing then cleaning means the commit split describes
code you already threw away, and the PR body describes a diff that no longer
exists.

## Stop conditions

- UI work: don't start until the user likes the UI.
- Nothing to clean is a valid outcome — say so in one line and go to step 2.
- Don't stall on a clean pass. If polish keeps expanding, that's scope creep;
  ship the narrow version.

## Scope

- **In:** polish the diff, shape commits, create or update the PR/MR, merge it
  and pull the default branch when asked, print the link.
- **Out:** fixing CI and review threads (`pr-ready`), merging nobody asked for.
