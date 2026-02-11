# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-11

### Added
- Initial release of Coopernico Home Assistant Integration
- Real-time Coopernico electricity price sensor
- Daily average price sensors (today and tomorrow)
- 48 hourly price sensors (24 for today, 24 for tomorrow)
- 192 15-minute interval price sensors (96 for today, 96 for tomorrow)
- Automatic OMIE data fetching from Iberian electricity market
- Bundled loss profile integration (perfil_perda_2026.xlsx)
- Configurable margin and GO (Guarantees of Origin) values
- Support for multiple tariff types (SIMPLES, BI-HORÁRIA, TRI-HORÁRIA)
- Automatic hourly data updates
- Comprehensive sensor attributes with hourly prices

### Features
- Fetches Portuguese marginal electricity prices from OMIE
- Calculates Coopernico prices using formula: (OMIE + margin) × (1 + loss_factor) + GO
- Applies network loss factors from bundled Excel file
- Provides 243 total sensors for comprehensive price monitoring
- All sensors update automatically every hour
