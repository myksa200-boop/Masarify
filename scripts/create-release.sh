#!/usr/bin/env bash
# =============================================================================
# Masarify - GitHub Release Script
# =============================================================================
# Usage:
#   1. Set up a GitHub repo and push:
#        git remote add origin https://github.com/YOUR_USER/masarify.git
#        git push -u origin main
#
#   2. Create and push a tag to trigger a release:
#        ./scripts/create-release.sh v1.0.0
#
#   The GitHub Actions workflow will build the APK and attach it to the release.
# =============================================================================

set -euo pipefail

TAG="${1:-}"

if [ -z "$TAG" ]; then
    echo "❌ Usage: $0 <tag>"
    echo "   Example: $0 v1.0.0"
    exit 1
fi

# Validate tag format
if [[ ! "$TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "⚠️  Tag should follow semantic versioning: vMAJOR.MINOR.PATCH"
    echo "   Example: v1.0.0, v1.1.0, v2.0.0"
fi

echo "🔖 Creating tag: $TAG"
git tag -a "$TAG" -m "Release $TAG"
git push origin "$TAG"

echo ""
echo "✅ Tag $TAG pushed!"
echo ""
echo "📱 Now go to GitHub → Actions to watch the build:"
echo "   https://github.com/YOUR_USER/masarify/actions"
echo ""
echo "📦 When done, download the APK from the release page:"
echo "   https://github.com/YOUR_USER/masarify/releases/tag/$TAG"
