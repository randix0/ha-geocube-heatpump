from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import BINARY_SENSORS, DOMAIN
from .entity import CarelEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(CarelBinarySensor(coord, entry, *b) for b in BINARY_SENSORS)


class CarelBinarySensor(CarelEntity, BinarySensorEntity):
    def __init__(self, coordinator, entry, key, name, dev_class):
        super().__init__(coordinator, entry, key, name)
        self._attr_device_class = dev_class

    @property
    def is_on(self):
        v = self._value
        return None if v is None else bool(v)
