# Branching and publishing

`main` is what people install. `dev` is where work lands first.

```
work ──► dev ──► main
         │        │
         │        └─ published: this is what `git clone` and `install.py` serve
         └─ integration: review and CI happen here
```

## The rule

- **Never commit to `main` directly.** Changes reach it only by merging `dev`.
- **`dev` takes the work.** Commit to `dev`, or open a short-lived branch against it when a change needs review.
- **Publishing is the `dev` → `main` merge.** Nothing else publishes.
- **CI must pass before either merge.** The `tests` check runs the installer suite, the publish guard, and both eval validators.

Both branches are public. `dev` is expected to be ahead of `main` between releases; a difference between them is normal, not an error.

## Feature branches

Optional but useful when a change is large enough to want review before it reaches `dev`:

```sh
git switch -c voice-workshop/field-lessons dev
# work, commit
git push origin voice-workshop/field-lessons
gh pr create --base dev
```

Merge that PR into `dev`, then delete the branch. Small changes can go straight to `dev`.

## What protects `main`

A repository ruleset named `main`, enforced for everyone including administrators:

| Rule | Why |
| --- | --- |
| Require a pull request before merging | Direct pushes to `main` are rejected, so publishing is always a reviewed merge |
| Required status check: `tests` | A red suite cannot be merged |
| Require branches to be up to date | The merge is tested against the current `main`, not a stale base |
| Require conversation resolution | An open review comment blocks the merge |
| Merge commits only | Squash and rebase would rewrite `dev`'s history; a merge commit records what shipped |
| Block force pushes | Rewritten history on a published branch breaks every clone |
| Block deletion | `main` cannot be removed by accident |

No required approvals: a solo maintainer cannot approve their own pull request, so requiring one would deadlock the repo. Review happens on the PR conversation and in CI.

`dev` carries a lighter ruleset: force pushes and deletion blocked, everything else allowed. It has to stay easy to commit to.

## Applying the rulesets

Requires admin on the repository. The `rapidanai` account owns it; a collaborator with write access cannot change rulesets.

```sh
gh auth switch            # to the account that owns rapidanai/skills
./scripts/protect-branches.sh
```

The script is idempotent: it updates the rulesets by name if they exist and creates them if they do not. To apply by hand, use **Settings → Rules → Rulesets**, and match the table above. Do not add a *Restrict updates* rule: without a bypass actor it blocks merges as well as pushes, which would leave `main` impossible to update.