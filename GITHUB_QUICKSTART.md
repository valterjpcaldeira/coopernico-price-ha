# Quick Start - Publishing to GitHub & HACS

## 🚀 Fast Track (5 minutes)

### Step 1: Run Setup Script

**Windows (PowerShell):**
```powershell
.\setup_github.ps1
```

**Linux/Mac:**
```bash
chmod +x setup_github.sh
./setup_github.sh
```

The script will:
- ✅ Initialize git repository
- ✅ Update manifest.json with your GitHub username
- ✅ Create initial commit
- ✅ Set up remote connection

### Step 2: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `coopernico-price-ha`
3. Description: `Home Assistant integration for Coopernico electricity prices`
4. **Visibility: Public** ⚠️ (required for HACS)
5. **DO NOT** check "Add a README file"
6. Click **Create repository**

### Step 3: Push to GitHub

```bash
git push -u origin main
```

### Step 4: Create Release

```bash
git tag -a v1.0.0 -m "Initial release v1.0.0"
git push origin v1.0.0
```

Then on GitHub:
1. Go to **Releases** → **Create a new release**
2. Tag: `v1.0.0`
3. Title: `v1.0.0 - Initial Release`
4. Click **Publish release**

### Step 5: Submit to HACS

1. Go to: https://github.com/hacs/default/issues/new
2. Choose **Integration** template
3. Repository URL: `https://github.com/YOUR_USERNAME/coopernico-price-ha`
4. Submit!

## 📋 Manual Steps (if script doesn't work)

### 1. Initialize Git

```bash
git init
git add .
git commit -m "Initial commit: Coopernico Home Assistant Integration v1.0.0"
git branch -M main
```

### 2. Update manifest.json

Edit `custom_components/coopernico/manifest.json`:
- Replace `valterjpcaldeira` with your GitHub username (3 places)

### 3. Connect to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/coopernico-price-ha.git
git push -u origin main
```

### 4. Create Release

```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

## ✅ Verification

After publishing, verify:

- [ ] Repository is public
- [ ] All files are pushed
- [ ] Release v1.0.0 exists
- [ ] README displays correctly
- [ ] manifest.json has correct URLs

## 🎯 Next Steps

1. **Wait for HACS approval** (usually 1-7 days)
2. **Share with community**:
   - Home Assistant Community Forum
   - Reddit r/homeassistant
   - Add GitHub topics: `home-assistant`, `integration`, `coopernico`

## 📖 Full Guide

See [PUBLISH_GUIDE.md](PUBLISH_GUIDE.md) for detailed instructions.
