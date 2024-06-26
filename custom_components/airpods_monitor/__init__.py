"""The AirPods Monitor integration."""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .sensor import get_data

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AirPods Monitor from a config entry."""
    coordinator = AirPodsDataUpdateCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault("airpods_monitor", {})[entry.entry_id] = coordinator

    hass.helpers.discovery.load_platform("sensor", "airpods_monitor", {}, entry)

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
            return await hass.async_add_executor_job(get_data)
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
