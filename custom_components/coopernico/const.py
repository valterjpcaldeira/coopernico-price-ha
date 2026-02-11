"""Constants for the Coopernico integration."""
from __future__ import annotations

from datetime import timedelta

DOMAIN = "coopernico"

# Default values from your app.py
DEFAULT_MARGIN_K = 0.009  # Coopernico margin €/kWh
DEFAULT_GO_VALUE = 0.001  # Guarantees of Origin €/kWh
DEFAULT_TSE = 0.0028930

# Update interval
UPDATE_INTERVAL = timedelta(hours=1)

# Timezone
LISBON_TZ = "Europe/Lisbon"

# Configuration keys
CONF_MARGIN_K = "margin_k"
CONF_GO_VALUE = "go_value"
CONF_TARIFA = "tarifa"
CONF_DIARIO = "diario"
CONF_GO_ENABLED = "go_enabled"

# Tariff options (from your app.py)
TARIFA_OPTIONS = ["SIMPLES", "BI-HORÁRIA", "TRI-HORÁRIA"]
