# Coopernico Price Home Assistant Integration

Home Assistant integration for Coopernico electricity prices. This integration fetches OMIE (Iberian electricity market) data and calculates Coopernico prices based on your configuration.

## Features

- 💶 **Current Price**: Real-time Coopernico electricity price (€/kWh)
- 📈 **Daily Averages**: Today's and tomorrow's average prices
- 🕐 **Hourly Prices**: Hour-by-hour prices available as sensor attributes
- ⚙️ **Configurable**: Set your margin, GO (Guarantees of Origin) value, and tariff type

## Installation

### Quick Start

1. **Copy the integration folder** to your Home Assistant config:
   ```bash
   cp -r custom_components/coopernico /config/custom_components/
   ```

2. **Restart Home Assistant**

3. **Add Integration**:
   - Go to **Settings** → **Devices & Services** → **Add Integration**
   - Search for "Coopernico Price"
   - Complete the setup wizard

📖 **Detailed instructions**: See [INSTALLATION.md](INSTALLATION.md)

🧪 **Testing**: See [TESTING.md](TESTING.md) for testing guide and troubleshooting

## Configuration

During setup, you can configure:

- **Margin (€/kWh)**: Coopernico margin (default: 0.009)
- **GO Value (€/kWh)**: Guarantees of Origin value (default: 0.001)
- **Tariff**: Choose between SIMPLES, BI-HORÁRIA, or TRI-HORÁRIA
- **Diário**: Daily tariff option (default: True)
- **GO Enabled**: Enable Guarantees of Origin (default: False)

## Sensors

The integration provides the following sensors:

### Main Sensors

| Sensor | Unit | Description |
|--------|------|-------------|
| `sensor.coopernico_current_price` | €/kWh | Current Coopernico price |
| `sensor.coopernico_daily_average_today` | €/kWh | Today's average price |
| `sensor.coopernico_daily_average_tomorrow` | €/kWh | Tomorrow's average price |

### Hourly Sensors

For each hour (00-23) and each day (today/tomorrow), there are individual sensors:

- `sensor.coopernico_hourly_today_H00` through `sensor.coopernico_hourly_today_H23`
- `sensor.coopernico_hourly_tomorrow_H00` through `sensor.coopernico_hourly_tomorrow_H23`

**Total: 48 hourly sensors** (24 for today + 24 for tomorrow)

Each hourly sensor shows the average price for that hour in €/kWh.

### 15-Minute Interval Sensors

For each 15-minute interval (00, 15, 30, 45) of each hour (00-23) and each day (today/tomorrow):

- `sensor.coopernico_15min_today_00:00` through `sensor.coopernico_15min_today_23:45`
- `sensor.coopernico_15min_tomorrow_00:00` through `sensor.coopernico_15min_tomorrow_23:45`

**Total: 192 15-minute sensors** (96 for today + 96 for tomorrow)

Each 15-minute sensor shows the price for that specific 15-minute interval in €/kWh.

### Sensor Attributes

Main sensors include attributes with hourly prices:
- `hourly_today`: Hourly prices for today (H00-H23)
- `hourly_tomorrow`: Hourly prices for tomorrow (H00-H23)
- `last_update`: Timestamp of last data update

Hourly and 15-minute sensors include:
- `hour`: Hour (0-23)
- `minute`: Minute (0, 15, 30, 45) for 15-minute sensors
- `day`: "today" or "tomorrow"
- `datetime`: ISO format datetime for the interval
- `last_update`: Timestamp of last data update

## Price Calculation

The Coopernico price is calculated using the formula:

```
Coopernico Price = (OMIE Price + Margin) × (1 + Loss Factor) + GO Value
```

Where:
- **OMIE Price**: Portuguese marginal electricity price from OMIE market (€/kWh)
- **Margin**: Your configured Coopernico margin (default: 0.009 €/kWh)
- **Loss Factor**: Network loss factor (BT - low voltage) from bundled loss profile file (`perfil_perda_2026.xlsx`)
- **GO Value**: Guarantees of Origin value if enabled (default: 0.001 €/kWh)

### Loss Profile

The integration includes a bundled loss profile file (`perfil_perda_2026.xlsx`) that contains network loss factors for different voltage levels (BT, MT, AT, AT/RT) at 15-minute intervals. The integration automatically uses the BT (low voltage) loss factor to calculate accurate Coopernico prices.

The loss profile file is automatically loaded from the integration directory - no manual configuration needed!

## Data Updates

The integration updates data every hour automatically. OMIE publishes day-ahead prices around 10:30 PM each day.

## Requirements

- Home Assistant 2024.1 or later
- Python packages:
  - `omie-market-data==0.1.0`
  - `pandas>=2.0.0`

## Development

This integration is based on the Coopernico analytics code and follows the same price calculation logic as the original Dash application.

## License

[Add your license here]

## Testing

Before installing in Home Assistant, you can test the integration:

```bash
python test_integration.py
```

This will verify:
- ✅ Dependencies are installed
- ✅ OMIE API connection works
- ✅ Loss profile file loads correctly
- ✅ Price calculation logic is correct

See [TESTING.md](TESTING.md) for detailed testing instructions.

## Next Steps

1. **Install the integration** (see [INSTALLATION.md](INSTALLATION.md))
2. **Test it** (see [TESTING.md](TESTING.md))
3. **Create automations** using the sensors
4. **Build dashboards** to visualize prices

## Support

For issues and feature requests, please open an issue on GitHub.
