"""Base entity."""
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class CarelEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, key: str, name: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Тепловий насос",
            manufacturer="Geocube",
            model="Heat pump (Carel pCOWeb)",
        )

    @property
    def available(self) -> bool:
        return super().available and self._key in (self.coordinator.data or {})

    @property
    def _value(self):
        return (self.coordinator.data or {}).get(self._key)
