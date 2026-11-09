from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberMode
from homeassistant.const import UnitOfTemperature

from .const import DOMAIN, NUMBERS
from .entity import CarelEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(CarelNumber(coord, entry, *n) for n in NUMBERS)


class CarelNumber(CarelEntity, NumberEntity):
    _attr_device_class = NumberDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator, entry, key, name, vmin, vmax, step):
        super().__init__(coordinator, entry, key, name)
        self._attr_native_min_value = vmin
        self._attr_native_max_value = vmax
        self._attr_native_step = step

    @property
    def native_value(self):
        return self._value

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_set_var(self._key, round(value, 2))
