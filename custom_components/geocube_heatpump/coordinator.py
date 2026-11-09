"""Data coordinator."""
from __future__ import annotations

import logging
from datetime import timedelta

from aiohttp import ClientError
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import CarelApi
from .const import ALL_VARS, DOMAIN

_LOGGER = logging.getLogger(__name__)


class CarelCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, api: CarelApi, scan_interval: int) -> None:
        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=scan_interval)
        )
        self.api = api
        self._missing: set[str] = set()

    async def _async_update_data(self):
        try:
            data = await self.api.get_vars(ALL_VARS)
        except (ClientError, TimeoutError) as err:
            raise UpdateFailed(f"Помилка зв'язку з контролером: {err}") from err

        missing = set(ALL_VARS) - data.keys()
        if missing and missing != self._missing:
            _LOGGER.warning("Контролер не повернув змінні: %s", ", ".join(sorted(missing)))
        self._missing = missing
        return data

    async def async_set_var(self, name: str, value) -> None:
        await self.api.set_var(name, value)
        # оптимістичне оновлення, потім справжнє читання
        if self.data is not None:
            self.data[name] = bool(value) if isinstance(value, bool) else value
            self.async_set_updated_data(self.data)
        await self.async_request_refresh()
