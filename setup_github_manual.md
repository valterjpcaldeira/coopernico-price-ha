# Manual GitHub Setup (No Script Needed)

Since PowerShell execution policy is blocking the script, here are the manual commands:

## Step 1: Initialize Git

```powershell
git init
git add .
git commit -m "Initial commit: Coopernico Home Assistant Integration v1.0.0"
git branch -M main
```

## Step 2: Update manifest.json

**Before pushing, you MUST update the GitHub username in manifest.json:**

1. Open `custom_components\coopernico\manifest.json` in a text editor
2. Replace `valterjpcaldeira` with your GitHub username in these 3 places:
   - Line 4: `"codeowners": ["@YOUR_USERNAME"]`
   - Line 7: `"documentation": "https://github.com/YOUR_USERNAME/coopernico-price-ha"`
   - Line 10: `"issue_tracker": "https://github.com/YOUR_USERNAME/coopernico-price-ha/issues"`

## Step 3: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `coopernico-price-ha`
3. Description: `Home Assistant integration for Coopernico electricity prices`
4. **Visibility: Public** ⚠️ (required for HACS)
5. **DO NOT** check "Add a README file"
6. Click **Create repository**

## Step 4: Connect and Push

```powershell
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/coopernico-price-ha.git
git push -u origin main
```

## Step 5: Create Release

```powershell
git tag -a v1.0.0 -m "Initial release v1.0.0"
git push origin v1.0.0
```

## Step 6: Create GitHub Release

1. Go to your repository on GitHub
2. Click **Releases** → **Create a new release**
3. Tag: `v1.0.0`
4. Title: `v1.0.0 - Initial Release`
5. Description:
   ```
   ## Initial Release
   
   First release of Coopernico Home Assistant Integration.
   
   ### Features
   - Real-time Coopernico electricity prices
   - 243 sensors (3 main + 48 hourly + 192 15-minute)
   - Automatic loss profile integration
   - Configurable margin and GO values
   ```
6. Click **Publish release**

## Step 7: Submit to HACS

1. Go to: https://github.com/hacs/default/issues/new
2. Choose **Integration** template
3. Repository URL: `https://github.com/YOUR_USERNAME/coopernico-price-ha`
4. Submit!

Done! 🎉
