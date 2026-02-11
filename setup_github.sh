#!/bin/bash
# GitHub Setup Script for Coopernico Integration
# Run this script to initialize git and prepare for GitHub push

echo "🚀 Coopernico Integration - GitHub Setup"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if already a git repository
if [ -d .git ]; then
    echo "⚠️  Git repository already initialized"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username is required"
    exit 1
fi

# Get repository name
read -p "Enter repository name (default: coopernico-price-ha): " REPO_NAME
REPO_NAME=${REPO_NAME:-coopernico-price-ha}

echo ""
echo "📝 Configuration:"
echo "   GitHub Username: $GITHUB_USERNAME"
echo "   Repository Name: $REPO_NAME"
echo ""

read -p "Continue with setup? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Initialize git if not already done
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Update manifest.json with GitHub username
echo "✏️  Updating manifest.json with your GitHub username..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/valterjpcaldeira/$GITHUB_USERNAME/g" custom_components/coopernico/manifest.json
else
    # Linux
    sed -i "s/valterjpcaldeira/$GITHUB_USERNAME/g" custom_components/coopernico/manifest.json
fi

# Add all files
echo "📁 Adding files to git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Coopernico Home Assistant Integration v1.0.0"

# Create main branch
echo "🌿 Setting up main branch..."
git branch -M main

# Add remote
echo "🔗 Adding GitHub remote..."
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git 2>/dev/null || \
git remote set-url origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git

echo ""
echo "✅ Git repository initialized!"
echo ""
echo "📋 Next steps:"
echo "   1. Create repository on GitHub: https://github.com/new"
echo "      Name: $REPO_NAME"
echo "      Visibility: Public"
echo "      DO NOT initialize with README/license"
echo ""
echo "   2. Push to GitHub:"
echo "      git push -u origin main"
echo ""
echo "   3. Create release tag:"
echo "      git tag -a v1.0.0 -m 'Initial release'"
echo "      git push origin v1.0.0"
echo ""
echo "   4. Submit to HACS:"
echo "      https://github.com/hacs/default/issues/new"
echo ""
echo "📖 See PUBLISH_GUIDE.md for detailed instructions"
