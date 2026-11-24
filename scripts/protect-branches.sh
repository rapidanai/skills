#!/usr/bin/env bash
# Apply branch rulesets to rapidanai/skills.
#
# Requires admin on the repository. The repo is owned by the `rapidanai` account;
# a collaborator with write access gets HTTP 404 from the rulesets API.
#
#   gh auth switch            # to the owning account
#   ./scripts/protect-branches.sh
#
# Idempotent: updates each ruleset if one with that name exists, creates it otherwise.
set -euo pipefail

REPO="${1:-rapidanai/skills}"

main_payload=$(cat <<'JSON'
{
  "name": "main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": { "include": ["refs/heads/main"], "exclude": [] }
  },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": true,
        "required_reviewers": [],
        "allowed_merge_methods": ["merge"]
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "required_status_checks": [{ "context": "tests" }]
      }
    }
  ],
  "bypass_actors": []
}
JSON
)

dev_payload=$(cat <<'JSON'
{
  "name": "dev",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": { "include": ["refs/heads/dev"], "exclude": [] }
  },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" }
  ],
  "bypass_actors": []
}
JSON
)

apply() {
  local name="$1" payload="$2"
  local id
  id=$(gh api "repos/$REPO/rulesets" --jq ".[] | select(.name==\"$name\") | .id" 2>/dev/null || true)
  if [ -n "$id" ]; then
    printf '%s' "$payload" | gh api --method PUT "repos/$REPO/rulesets/$id" --input - >/dev/null
    echo "updated ruleset: $name (id $id)"
  else
    printf '%s' "$payload" | gh api --method POST "repos/$REPO/rulesets" --input - >/dev/null
    echo "created ruleset: $name"
  fi
}

if ! gh api "repos/$REPO" --jq '.permissions.admin' | grep -q true; then
  echo "error: this account does not have admin on $REPO." >&2
  echo "       repos are administered by the account that owns them; switch with 'gh auth switch'." >&2
  echo "       current: $(gh api "repos/$REPO" --jq '.permissions | to_entries | map(select(.value)) | map(.key) | join(\",\")' 2>/dev/null || echo unknown)" >&2
  exit 1
fi

apply main "$main_payload"
apply dev "$dev_payload"

echo
gh api "repos/$REPO/rulesets" --jq '.[] | "\(.name): \(.enforcement)"'