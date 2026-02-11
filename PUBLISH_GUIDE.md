# Publishing Guide - GitHub & HACS

This guide will walk you through publishing your Coopernico integration to GitHub and HACS.

## 📋 Prerequisites

- GitHub account
- Git installed on your computer
- Basic knowledge of Git commands

## 🚀 Step 1: Initialize Git Repository

### 1.1 Initialize Git

```bash
# Navigate to your project directory
cd c:\Users\valte\Documents\GitHub\coopernico-price-ha

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Coopernico Home Assistant Integration v1.0.0"
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `coopernico-price-ha` (or your preferred name)
3. Description: `Home Assistant integration for Coopernico electricity prices - OMIE market data with loss profiles`
4. Visibility: **Public** (required for HACS)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

### 1.3 Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/coopernico-price-ha.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## 📝 Step 2: Update Repository URLs

Before pushing, update the URLs in `manifest.json`:

1. Open `custom_components/coopernico/manifest.json`
2. Replace `valterjpcaldeira` with your GitHub username in:
   - `codeowners`
   - `documentation` URL
   - `issue_tracker` URL

Example:
```json
{
  "codeowners": ["@yourusername"],
  "documentation": "https://github.com/yourusername/coopernico-price-ha",
  "issue_tracker": "https://github.com/yourusername/coopernico-price-ha/issues"
}
```

## 🏷️ Step 3: Create First Release

### 3.1 Create Release Tag

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Initial release v1.0.0"

# Push tag to GitHub
git push origin v1.0.0
```

### 3.2 Create GitHub Release

1. Go to your repository on GitHub
2. Click **Releases** → **Create a new release**
3. Choose tag: `v1.0.0`
4. Release title: `v1.0.0 - Initial Release`
5. Description:
   ```markdown
   ## Initial Release
   
   First release of Coopernico Home Assistant Integration.
   
   ### Features
   - Real-time Coopernico electricity prices
   - 243 sensors (3 main + 48 hourly + 192 15-minute)
   - Automatic loss profile integration
   - Configurable margin and GO values
   
   ### Installation
   See README.md for installation instructions.
   ```
6. Click **Publish release**

## 🎯 Step 4: Submit to HACS

### 4.1 HACS Requirements Checklist

Before submitting, verify:

- ✅ Repository is **public**
- ✅ `hacs.json` file exists (already created)
- ✅ `README.md` exists (already created)
- ✅ Repository has at least one release/tag
- ✅ Integration follows Home Assistant structure
- ✅ `manifest.json` is valid

### 4.2 Submit to HACS

1. Go to https://github.com/hacs/default
2. Click **Issues** → **New Issue**
3. Choose **Integration** template
4. Fill in the form:

   **Repository URL:**
   ```
   https://github.com/YOUR_USERNAME/coopernico-price-ha
   ```

   **Description:**
   ```
   Home Assistant integration for Coopernico electricity prices.
   
   Features:
   - Fetches OMIE (Iberian electricity market) data
   - Calculates Coopernico prices with loss profiles
   - Provides 243 sensors (current, hourly, 15-minute intervals)
   - Configurable margin and GO values
   - Automatic updates every hour
   
   The integration includes bundled loss profile data for accurate price calculations.
   ```

5. Submit the issue

### 4.3 HACS Review Process

- HACS maintainers will review your submission
- They may ask questions or request changes
- Review typically takes a few days to a week
- Once approved, your integration will be available in HACS

## 📦 Step 5: Alternative - Manual HACS Installation

Users can install via HACS manually before official approval:

1. Open HACS → **Integrations**
2. Click **⋮** (three dots) → **Custom repositories**
3. Add:
   - **Repository**: `https://github.com/YOUR_USERNAME/coopernico-price-ha`
   - **Category**: **Integration**
4. Click **Add**
5. Search for "Coopernico" and install

## 🔄 Step 6: Future Updates

### Creating New Releases

```bash
# Update version in manifest.json
# Then:
git add .
git commit -m "Update to v1.0.1"
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin main
git push origin v1.0.1
```

### Updating HACS Users

- HACS automatically checks for new releases
- Users will see update notifications
- They can update via HACS UI

## 📊 Step 7: Promote Your Integration

After publishing:

1. **Home Assistant Community**:
   - Post in https://community.home-assistant.io/
   - Share in the "Integrations" category

2. **Reddit**:
   - r/homeassistant
   - r/homeautomation

3. **GitHub**:
   - Add topics: `home-assistant`, `home-assistant-integration`, `coopernico`, `electricity`, `portugal`, `omie`

4. **Documentation**:
   - Keep README updated
   - Add examples and use cases
   - Respond to issues promptly

## ✅ Verification Checklist

Before submitting to HACS:

- [ ] Repository is public
- [ ] All files committed and pushed
- [ ] At least one release/tag created
- [ ] `manifest.json` URLs updated with your GitHub username
- [ ] `README.md` is complete and accurate
- [ ] `hacs.json` exists and is valid
- [ ] Integration tested and working
- [ ] No sensitive data in repository
- [ ] LICENSE file included

## 🆘 Troubleshooting

### Git Push Errors

**Authentication:**
```bash
# Use GitHub CLI or Personal Access Token
# Or use SSH instead of HTTPS
git remote set-url origin git@github.com:YOUR_USERNAME/coopernico-price-ha.git
```

**Permission Denied:**
- Check you have write access to the repository
- Verify your GitHub credentials

### HACS Rejection

Common reasons:
- Missing `hacs.json`
- Invalid `manifest.json`
- Repository not public
- Missing release/tag

Fix issues and resubmit.

## 📚 Additional Resources

- **HACS Documentation**: https://hacs.xyz/docs/publish/integration
- **Home Assistant Integration Guide**: https://developers.home-assistant.io/docs/creating_integration_manifest
- **GitHub Guides**: https://guides.github.com/

## 🎉 Success!

Once published:
- Users can install via HACS
- You'll receive stars and feedback
- Community can contribute via issues/PRs
- You can track usage via GitHub insights

Good luck! 🚀
