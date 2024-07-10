from homeassistant.components.sensor import SensorEntity
from .airpods import get_data

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([
        AirPodsBatterySensor("AirPods Left Battery"),
        AirPodsBatterySensor("AirPods Right Battery"),
        AirPodsBatterySensor("AirPods Case Battery"),
    ])

class AirPodsBatterySensor(SensorEntity):

    def __init__(self, name):
        self._name = name
        self._state = None
        self._attr = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attr

    def update(self):
        data = get_data()
        if data["status"] == 1:
            self._attr = data
            if self._name == "AirPods Left Battery":
                self._state = data["charge"]["left"]
            elif self._name == "AirPods Right Battery":
                self._state = data["charge"]["right"]
            elif self._name == "AirPods Case Battery":
                self._state = data["charge"]["case"]
