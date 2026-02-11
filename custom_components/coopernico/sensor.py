"""Sensor platform for Coopernico."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import CoopernicoDataUpdateCoordinator

LISBON_TZ = ZoneInfo("Europe/Lisbon")

SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="current_price",
        name="Coopernico Current Price",
        native_unit_of_measurement="€/kWh",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:currency-eur",
    ),
    SensorEntityDescription(
        key="daily_average_today",
        name="Coopernico Daily Average (Today)",
        native_unit_of_measurement="€/kWh",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="daily_average_tomorrow",
        name="Coopernico Daily Average (Tomorrow)",
        native_unit_of_measurement="€/kWh",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:chart-line",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Coopernico sensor entities."""
    coordinator: CoopernicoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        CoopernicoSensor(coordinator, description) for description in SENSOR_DESCRIPTIONS
    ]

    # Add hourly sensors for today and tomorrow (H00-H23)
    for day in ["today", "tomorrow"]:
        for hour in range(24):
            entities.append(
                CoopernicoHourlySensor(coordinator, hour, day)
            )

    # Add 15-minute interval sensors for today and tomorrow
    for day in ["today", "tomorrow"]:
        for hour in range(24):
            for minute in [0, 15, 30, 45]:
                entities.append(
                    Coopernico15MinSensor(coordinator, hour, minute, day)
                )

    async_add_entities(entities)


class CoopernicoSensor(CoordinatorEntity[CoopernicoDataUpdateCoordinator], SensorEntity):
    """Representation of a Coopernico sensor."""

    def __init__(
        self,
        coordinator: CoopernicoDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{description.key}"
        self._attr_name = f"{coordinator.entry.title} {description.name}"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None

        value = self.coordinator.data.get(self.entity_description.key)
        return round(value, 4) if value is not None else None

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional state attributes."""
        if self.coordinator.data is None:
            return {}

        attrs = {
            "last_update": self.coordinator.data.get("last_update"),
            "current_datetime": self.coordinator.data.get("current_datetime"),
        }

        # Add hourly prices as attributes
        if self.entity_description.key == "current_price":
            attrs["hourly_today"] = self.coordinator.data.get("hourly_today", {})
            attrs["hourly_tomorrow"] = self.coordinator.data.get("hourly_tomorrow", {})
        elif self.entity_description.key == "daily_average_today":
            attrs["hourly_prices"] = self.coordinator.data.get("hourly_today", {})
        elif self.entity_description.key == "daily_average_tomorrow":
            attrs["hourly_prices"] = self.coordinator.data.get("hourly_tomorrow", {})

        return attrs


class CoopernicoHourlySensor(CoordinatorEntity[CoopernicoDataUpdateCoordinator], SensorEntity):
    """Representation of a Coopernico hourly price sensor."""

    def __init__(
        self,
        coordinator: CoopernicoDataUpdateCoordinator,
        hour: int,
        day: str,
    ) -> None:
        """Initialize the hourly sensor."""
        super().__init__(coordinator)
        self.hour = hour
        self.day = day
        self._attr_unique_id = f"{coordinator.entry.entry_id}_hourly_{day}_H{hour:02d}"
        day_label = "Today" if day == "today" else "Tomorrow"
        self._attr_name = f"{coordinator.entry.title} Hourly {day_label} H{hour:02d}"
        self._attr_native_unit_of_measurement = "€/kWh"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:clock-outline"

    @property
    def native_value(self) -> float | None:
        """Return the hourly price."""
        if self.coordinator.data is None:
            return None

        hourly_key = f"hourly_{self.day}"
        hourly_data = self.coordinator.data.get(hourly_key, {})
        price_key = f"H{self.hour:02d}"
        value = hourly_data.get(price_key)
        return round(value, 4) if value is not None else None

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional state attributes."""
        if self.coordinator.data is None:
            return {}

        return {
            "hour": self.hour,
            "day": self.day,
            "last_update": self.coordinator.data.get("last_update"),
        }


class Coopernico15MinSensor(CoordinatorEntity[CoopernicoDataUpdateCoordinator], SensorEntity):
    """Representation of a Coopernico 15-minute interval price sensor."""

    def __init__(
        self,
        coordinator: CoopernicoDataUpdateCoordinator,
        hour: int,
        minute: int,
        day: str,
    ) -> None:
        """Initialize the 15-minute sensor."""
        super().__init__(coordinator)
        self.hour = hour
        self.minute = minute
        self.day = day
        self._attr_unique_id = (
            f"{coordinator.entry.entry_id}_15min_{day}_H{hour:02d}M{minute:02d}"
        )
        day_label = "Today" if day == "today" else "Tomorrow"
        self._attr_name = (
            f"{coordinator.entry.title} 15min {day_label} {hour:02d}:{minute:02d}"
        )
        self._attr_native_unit_of_measurement = "€/kWh"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:clock-time-four-outline"

    @property
    def native_value(self) -> float | None:
        """Return the 15-minute interval price."""
        if self.coordinator.data is None:
            return None

        interval_key = f"interval_15min_{self.day}"
        interval_data = self.coordinator.data.get(interval_key, {})
        price_key = f"H{self.hour:02d}M{self.minute:02d}"
        value = interval_data.get(price_key)
        return round(value, 4) if value is not None else None

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional state attributes."""
        if self.coordinator.data is None:
            return {}

        # Calculate the actual datetime for this interval
        today = date.today()
        target_date = today if self.day == "today" else today + timedelta(days=1)
        interval_datetime = datetime.combine(
            target_date, datetime.min.time().replace(hour=self.hour, minute=self.minute)
        )

        return {
            "hour": self.hour,
            "minute": self.minute,
            "day": self.day,
            "datetime": interval_datetime.isoformat(),
            "last_update": self.coordinator.data.get("last_update"),
        }
