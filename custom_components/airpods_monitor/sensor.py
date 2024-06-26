"""Sensor platform for AirPods Monitor."""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN
from homeassistant.helpers.entity_platform import async_add_entities

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the AirPods Monitor sensor."""
    coordinator = hass.data["airpods_monitor"]

    async_add_entities([AirPodsSensor(coordinator)], True)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up AirPods Monitor sensor from a config entry."""
    coordinator = hass.data["airpods_monitor"][entry.entry_id]

    async_add_entities([AirPodsSensor(coordinator)], True)

class AirPodsSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._state = STATE_UNKNOWN
        self._data = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return "AirPods Monitor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._data

    async def async_update(self):
        """Fetch new state data for the sensor."""
        await self._coordinator.async_request_refresh()
        data = self._coordinator.data
        self._data = data
        self._state = data.get("status", STATE_UNKNOWN)
