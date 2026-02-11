# Next Commands - Complete GitHub Setup

## ✅ Already Done

- ✅ Git repository initialized
- ✅ Files added and committed
- ✅ Branch renamed to `main`

## 📝 Step 1: Update manifest.json

**IMPORTANT:** Before pushing, update your GitHub username in `manifest.json`:

1. Open `custom_components\coopernico\manifest.json`
2. Replace `valterjpcaldeira` with **YOUR GitHub username** in 3 places:
   - Line 4: `"codeowners": ["@YOUR_USERNAME"]`
   - Line 7: `"documentation": "https://github.com/YOUR_USERNAME/coopernico-price-ha"`
   - Line 10: `"issue_tracker": "https://github.com/YOUR_USERNAME/coopernico-price-ha/issues"`

## 🚀 Step 2: Create GitHub Repository

1. Go to: **https://github.com/new**
2. Repository name: `coopernico-price-ha`
3. Description: `Home Assistant integration for Coopernico electricity prices`
4. **Visibility: Public** ⚠️ (required for HACS)
5. **DO NOT** check "Add a README file" or any other options
6. Click **Create repository**

## 📤 Step 3: Connect and Push

After creating the repository, run these commands (replace YOUR_USERNAME):

```powershell
git remote add origin https://github.com/YOUR_USERNAME/coopernico-price-ha.git
git push -u origin main
```

## 🏷️ Step 4: Create Release Tag

```powershell
git tag -a v1.0.0 -m "Initial release v1.0.0"
git push origin v1.0.0
```

## 📦 Step 5: Create GitHub Release

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

## 🎯 Step 6: Submit to HACS

1. Go to: **https://github.com/hacs/default/issues/new**
2. Choose **Integration** template
3. Repository URL: `https://github.com/YOUR_USERNAME/coopernico-price-ha`
4. Description:
   ```
   Home Assistant integration for Coopernico electricity prices.
   
   Features:
   - Fetches OMIE (Iberian electricity market) data
   - Calculates Coopernico prices with loss profiles
   - Provides 243 sensors (current, hourly, 15-minute intervals)
   - Configurable margin and GO values
   - Automatic hourly updates
   ```
5. Submit!

## ✅ Checklist

Before submitting to HACS:
- [ ] Updated manifest.json with your GitHub username
- [ ] Repository is Public
- [ ] Code pushed to GitHub
- [ ] Release tag v1.0.0 created
- [ ] GitHub release published

## 🎉 Done!

After HACS approval (usually 1-7 days), users can install your integration via HACS!
