from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass

from .const import DOMAIN, SENSORS
from .entity import CarelEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(CarelSensor(coord, entry, *s) for s in SENSORS)


class CarelSensor(CarelEntity, SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, entry, key, name, unit, dev_class):
        super().__init__(coordinator, entry, key, name)
        self._attr_native_unit_of_measurement = unit
        if dev_class == "temperature":
            self._attr_device_class = SensorDeviceClass.TEMPERATURE

    @property
    def native_value(self):
        v = self._value
        return round(v, 2) if isinstance(v, float) else v
