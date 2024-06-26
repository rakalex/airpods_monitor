"""The AirPods Monitor integration."""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .airpods import get_data

_LOGGER = logging.getLogger(__name__)

DOMAIN = "airpods_monitor"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AirPods Monitor from a config entry."""
    coordinator = AirPodsDataUpdateCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, ["sensor"])

    return True

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the AirPods Monitor component."""
    hass.data.setdefault(DOMAIN, {})

    if DOMAIN not in config:
        return True

    for entry in hass.config_entries.async_entries(DOMAIN):
        hass.async_create_task(
            hass.config_entries.async_setup_platforms(entry, ["sensor"])
        )

    return True

class AirPodsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching AirPods data."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="airpods_monitor",
            update_interval=timedelta(minutes=30),  # Run every 30 minutes
        )

    async def _async_update_data(self):
        """Fetch data from AirPods."""
        try:
            return await self.hass.async_add_executor_job(get_data)
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
