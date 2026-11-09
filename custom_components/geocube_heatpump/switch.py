from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, VAR_POWER
from .entity import CarelEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CarelPowerSwitch(coord, entry)])


class CarelPowerSwitch(CarelEntity, SwitchEntity):
    _attr_icon = "mdi:heat-pump"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry, VAR_POWER, "Вкл/викл")

    @property
    def is_on(self):
        v = self._value
        return None if v is None else bool(v)

    async def async_turn_on(self, **kwargs):
        await self.coordinator.async_set_var(VAR_POWER, 1)

    async def async_turn_off(self, **kwargs):
        await self.coordinator.async_set_var(VAR_POWER, 0)
