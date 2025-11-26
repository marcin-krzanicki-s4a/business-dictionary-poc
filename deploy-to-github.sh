#!/bin/bash

# S4A Business Dictionary - Git Setup Script
# This script initializes the git repository and pushes to GitHub

set -e  # Exit on error

echo "🚀 Setting up Git repository for S4A Business Dictionary..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: git is not installed. Please install git first."
    exit 1
fi

# Check if already a git repository
if [ -d ".git" ]; then
    echo "⚠️  Git repository already exists."
    read -p "Do you want to continue? This will add files and push to remote. (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
else
    # Initialize git repository
    echo "📦 Initializing git repository..."
    git init
fi

# Add remote if not exists
REMOTE_URL="https://github.com/marcin-krzanicki-s4a/business-dictionary-poc.git"
if ! git remote | grep -q "origin"; then
    echo "🔗 Adding remote origin..."
    git remote add origin $REMOTE_URL
else
    echo "✓ Remote origin already exists"
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Commit
echo "💾 Creating commit..."
git commit -m "Initial commit: S4A Business Dictionary POC

Features:
- Business Objects with data lineage
- Perspectives and UI Views
- Interactive Mermaid diagrams
- Role-based filtering
- GitHub Pages deployment
" || echo "⚠️  No changes to commit or commit already exists"

# Get current branch name
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Rename to main if needed
if [ "$BRANCH" != "main" ]; then
    echo "🔄 Renaming branch to 'main'..."
    git branch -M main
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
echo "Note: You may need to authenticate with GitHub"
git push -u origin main

echo ""
echo "✅ Done! Your repository has been pushed to GitHub."
echo ""
echo "📋 Next steps:"
echo "1. Go to: https://github.com/marcin-krzanicki-s4a/business-dictionary-poc/settings/pages"
echo "2. Under 'Source', select 'GitHub Actions'"
echo "3. Wait for the deployment to complete (check Actions tab)"
echo "4. Your site will be available at:"
echo "   https://marcin-krzanicki-s4a.github.io/business-dictionary-poc/"
echo ""
