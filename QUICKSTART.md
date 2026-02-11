# Quick Start Guide

## 🚀 Installation Steps

### 1. Copy Integration Files

Copy the `custom_components/coopernico` folder to your Home Assistant configuration directory:

**Linux/Mac:**
```bash
cp -r custom_components/coopernico /config/custom_components/
```

**Windows (PowerShell):**
```powershell
Copy-Item -Recurse custom_components\coopernico C:\config\custom_components\
```

**Docker:**
```bash
docker cp custom_components/coopernico <container_name>:/config/custom_components/
```

### 2. Restart Home Assistant

- Go to **Settings** → **System** → **Hardware** → **Restart**
- Or use Developer Tools → YAML → Restart

### 3. Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration** (bottom right)
3. Search for **"Coopernico"**
4. Click on **Coopernico Price**
5. Configure:
   - **Name**: Coopernico Price (or your choice)
   - **Margin**: 0.009 €/kWh (default)
   - **GO Value**: 0.001 €/kWh (default)
   - **Tariff**: SIMPLES (or BI-HORÁRIA, TRI-HORÁRIA)
   - **Diário**: True
   - **GO Enabled**: False
6. Click **Submit**

### 4. Verify Installation

✅ Check **Settings** → **Devices & Services** → **Coopernico Price**  
✅ Verify **243 entities** are created  
✅ Check sensor values in **Developer Tools** → **States**

## 🧪 Testing Before Installation

Run the test script to verify everything works:

```bash
python test_integration.py
```

This will test:
- ✅ Dependencies
- ✅ OMIE API connection
- ✅ Loss profile file loading
- ✅ Price calculations

## 📊 What You Get

After installation, you'll have:

- **3 Main Sensors**:
  - Current price
  - Today's average
  - Tomorrow's average

- **48 Hourly Sensors**:
  - 24 for today (H00-H23)
  - 24 for tomorrow (H00-H23)

- **192 15-Minute Sensors**:
  - 96 for today (every 15 minutes)
  - 96 for tomorrow (every 15 minutes)

**Total: 243 sensors** 🎉

## 🔍 Quick Verification

Check if sensors are working:

```yaml
# In Developer Tools → States, search for:
sensor.coopernico_current_price
sensor.coopernico_hourly_today_H12
sensor.coopernico_15min_today_12_00
```

## 📝 Example Automation

```yaml
automation:
  - alias: "Notify Low Price"
    trigger:
      - platform: numeric_state
        entity_id: sensor.coopernico_current_price
        below: 0.10
    action:
      - service: notify.mobile_app
        data:
          message: "Low price: {{ states('sensor.coopernico_current_price') }} €/kWh"
```

## 🆘 Troubleshooting

**Integration not appearing?**
- ✅ Check file structure: `/config/custom_components/coopernico/`
- ✅ Verify all files are present (especially `manifest.json`)
- ✅ Check Home Assistant logs for errors
- ✅ Ensure you did a full restart (not just reload)

**Sensors not updating?**
- ✅ Check logs: Settings → System → Logs
- ✅ Verify internet connection (OMIE API needs internet)
- ✅ Wait a few minutes after installation

**Need more help?**
- See [TESTING.md](TESTING.md) for detailed troubleshooting
- See [INSTALLATION.md](INSTALLATION.md) for detailed installation steps
