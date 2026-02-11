"""Data update coordinator for Coopernico."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, UPDATE_INTERVAL
from .omie_client import CoopernicoOMIEClient

LISBON_TZ = ZoneInfo("Europe/Lisbon")


class CoopernicoDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Coopernico data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.entry = entry
        self.client = CoopernicoOMIEClient(
            margin_k=entry.data.get("margin_k", 0.009),
            go_value=entry.data.get("go_value", 0.001),
            tarifa=entry.data.get("tarifa", "SIMPLES"),
            diario=entry.data.get("diario", True),
            go_enabled=entry.data.get("go_enabled", False),
        )

        super().__init__(
            hass,
            logger=self.logger,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from OMIE and calculate Coopernico prices."""
        try:
            date_ini = date.today()
            date_end = date_ini + timedelta(days=7)

            data = await self.hass.async_add_executor_job(
                self.client.fetch_and_calculate_prices, date_ini, date_end
            )

            if not data:
                raise UpdateFailed("No data received from OMIE")

            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with OMIE: {err}") from err
