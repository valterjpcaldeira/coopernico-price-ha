# GitHub Setup Script for Coopernico Integration (PowerShell)
# Run this script to initialize git and prepare for GitHub push

Write-Host "🚀 Coopernico Integration - GitHub Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $null = git --version
} catch {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Check if already a git repository
if (Test-Path .git) {
    Write-Host "⚠️  Git repository already initialized" -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 1
    }
}

# Get GitHub username
$GITHUB_USERNAME = Read-Host "Enter your GitHub username"

if ([string]::IsNullOrWhiteSpace($GITHUB_USERNAME)) {
    Write-Host "❌ GitHub username is required" -ForegroundColor Red
    exit 1
}

# Get repository name
$REPO_NAME = Read-Host "Enter repository name (default: coopernico-price-ha)"
if ([string]::IsNullOrWhiteSpace($REPO_NAME)) {
    $REPO_NAME = "coopernico-price-ha"
}

Write-Host ""
Write-Host "📝 Configuration:" -ForegroundColor Cyan
Write-Host "   GitHub Username: $GITHUB_USERNAME"
Write-Host "   Repository Name: $REPO_NAME"
Write-Host ""

$continue = Read-Host "Continue with setup? (y/n)"
if ($continue -ne "y" -and $continue -ne "Y") {
    exit 1
}

# Initialize git if not already done
if (-not (Test-Path .git)) {
    Write-Host "📦 Initializing git repository..." -ForegroundColor Green
    git init
}

# Update manifest.json with GitHub username
Write-Host "✏️  Updating manifest.json with your GitHub username..." -ForegroundColor Green
$manifestPath = "custom_components\coopernico\manifest.json"
$manifestContent = Get-Content $manifestPath -Raw
$manifestContent = $manifestContent -replace "valterjpcaldeira", $GITHUB_USERNAME
Set-Content -Path $manifestPath -Value $manifestContent -NoNewline

# Add all files
Write-Host "📁 Adding files to git..." -ForegroundColor Green
git add .

# Create initial commit
Write-Host "💾 Creating initial commit..." -ForegroundColor Green
git commit -m "Initial commit: Coopernico Home Assistant Integration v1.0.0"

# Create main branch
Write-Host "🌿 Setting up main branch..." -ForegroundColor Green
git branch -M main

# Add remote
Write-Host "🔗 Adding GitHub remote..." -ForegroundColor Green
$remoteUrl = "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
try {
    git remote add origin $remoteUrl
} catch {
    git remote set-url origin $remoteUrl
}

Write-Host ""
Write-Host "✅ Git repository initialized!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Create repository on GitHub: https://github.com/new"
Write-Host "      Name: $REPO_NAME"
Write-Host "      Visibility: Public"
Write-Host "      DO NOT initialize with README/license"
Write-Host ""
Write-Host "   2. Push to GitHub:"
Write-Host "      git push -u origin main"
Write-Host ""
Write-Host "   3. Create release tag:"
Write-Host "      git tag -a v1.0.0 -m `"Initial release`""
Write-Host "      git push origin v1.0.0"
Write-Host ""
Write-Host "   4. Submit to HACS:"
Write-Host "      https://github.com/hacs/default/issues/new"
Write-Host ""
Write-Host "📖 See PUBLISH_GUIDE.md for detailed instructions" -ForegroundColor Yellow
