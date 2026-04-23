#!/usr/bin/env bash

set -e  # exit if any command fails

OLD_REMOTE="origin"
NEW_REMOTE="private"
NEW_REPO_URL="https://github.com/JD2112/jd2112-website.git"
BRANCH="website"

echo "🔍 Checking that branch '$BRANCH' exists locally..."
git rev-parse --verify "$BRANCH" >/dev/null

echo "➡️ Switching to branch '$BRANCH'..."
git checkout "$BRANCH"

echo "➕ Adding new private repo as remote '$NEW_REMOTE'..."
git remote add "$NEW_REMOTE" "$NEW_REPO_URL"

echo "🚀 Pushing branch '$BRANCH' to private repo..."
# Push it as 'main' in the new repo (recommended), OR:
git push "$NEW_REMOTE" "$BRANCH:main"

# If you prefer the same branch name in the new repo:
# git push "$NEW_REMOTE" "$BRANCH:$BRANCH"

echo "🧹 Deleting branch '$BRANCH' from public repo ($OLD_REMOTE)..."
git push "$OLD_REMOTE" --delete "$BRANCH"

echo "✔️ Transfer complete!"
echo "📌 '$BRANCH' now lives in: $NEW_REPO_URL"
echo "📌 And it has been removed from the public repo."
