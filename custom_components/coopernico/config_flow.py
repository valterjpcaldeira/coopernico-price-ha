"""Config flow for Coopernico integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_DIARIO,
    CONF_GO_ENABLED,
    CONF_GO_VALUE,
    CONF_MARGIN_K,
    CONF_TARIFA,
    DEFAULT_GO_VALUE,
    DEFAULT_MARGIN_K,
    DOMAIN,
    TARIFA_OPTIONS,
)


class CoopernicoConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Coopernico."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input.get(CONF_NAME, "Coopernico Price"),
                data=user_input,
            )

        data_schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default="Coopernico Price"): str,
                vol.Optional(CONF_MARGIN_K, default=DEFAULT_MARGIN_K): vol.Coerce(
                    float
                ),
                vol.Optional(CONF_GO_VALUE, default=DEFAULT_GO_VALUE): vol.Coerce(
                    float
                ),
                vol.Optional(CONF_TARIFA, default="SIMPLES"): vol.In(TARIFA_OPTIONS),
                vol.Optional(CONF_DIARIO, default=True): bool,
                vol.Optional(CONF_GO_ENABLED, default=False): bool,
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema)
