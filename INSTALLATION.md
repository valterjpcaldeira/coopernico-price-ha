# Installation Guide - Coopernico Home Assistant Integration

## Quick Start

### Option 1: Manual Installation (Recommended for Testing)

1. **Copy the integration folder**:
   ```bash
   # Copy custom_components/coopernico to your Home Assistant config directory
   cp -r custom_components/coopernico /config/custom_components/
   ```

2. **Restart Home Assistant**

3. **Add Integration**:
   - Go to **Settings** → **Devices & Services** → **Add Integration**
   - Search for "Coopernico"
   - Complete the setup wizard

### Option 2: HACS Installation (Future)

Once published to HACS:

1. Open **HACS** → **Integrations**
2. Click **Custom Repositories**
3. Add repository: `https://github.com/yourusername/coopernico-price-ha`
4. Install **Coopernico Price**
5. Restart Home Assistant
6. Add Integration from Devices & Services

## File Structure

```
/config/custom_components/coopernico/
├── __init__.py              # Integration initialization
├── manifest.json            # Integration metadata
├── config_flow.py          # Configuration UI
├── const.py                # Constants
├── coordinator.py          # Data update coordinator
├── omie_client.py          # OMIE API client
├── sensor.py               # Sensor entities
└── perfil_perda_2026.xlsx  # Loss profile data
```

## Requirements

- **Home Assistant**: 2024.1 or later
- **Python Packages** (installed automatically):
  - `omie-market-data==0.1.0`
  - `pandas>=2.0.0`
  - `openpyxl>=3.0.0`

## Configuration Options

During setup, you can configure:

| Option | Default | Description |
|--------|---------|-------------|
| **Margin (€/kWh)** | 0.009 | Coopernico margin |
| **GO Value (€/kWh)** | 0.001 | Guarantees of Origin value |
| **Tariff** | SIMPLES | Tariff type (SIMPLES, BI-HORÁRIA, TRI-HORÁRIA) |
| **Diário** | True | Daily tariff option |
| **GO Enabled** | False | Enable Guarantees of Origin |

## Verification

After installation:

1. Check **Settings** → **Devices & Services** → **Coopernico Price**
2. Verify **243 entities** are created
3. Check sensor values in **Developer Tools** → **States**
4. Monitor logs for any errors

## Updating the Integration

1. Stop Home Assistant
2. Replace files in `/config/custom_components/coopernico/`
3. Restart Home Assistant
4. The integration will auto-update

## Uninstallation

1. Go to **Settings** → **Devices & Services**
2. Find **Coopernico Price**
3. Click **Delete**
4. Remove the folder: `/config/custom_components/coopernico/`
5. Restart Home Assistant
