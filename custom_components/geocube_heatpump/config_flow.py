"""Config flow."""
from __future__ import annotations

import voluptuous as vol
from aiohttp import ClientError
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import CarelApi
from .const import (
    CONF_HOST,
    CONF_SCAN_INTERVAL,
    DEFAULT_HOST,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    VAR_POWER,
)


async def _check(hass, host: str) -> bool:
    data = await CarelApi(async_get_clientsession(hass), host).get_vars([VAR_POWER])
    return VAR_POWER in data


class CarelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            self._async_abort_entries_match({CONF_HOST: host})
            try:
                if await _check(self.hass, host):
                    return self.async_create_entry(title=f"Geocube {host}", data={CONF_HOST: host})
                errors["base"] = "invalid_response"
            except (ClientError, TimeoutError):
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST, default=DEFAULT_HOST): str}),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return CarelOptionsFlow()


class CarelOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        errors = {}
        entry = self.config_entry
        if user_input is not None:
            try:
                if await _check(self.hass, user_input[CONF_HOST].strip()):
                    return self.async_create_entry(data=user_input)
                errors["base"] = "invalid_response"
            except (ClientError, TimeoutError):
                errors["base"] = "cannot_connect"

        host = entry.options.get(CONF_HOST, entry.data[CONF_HOST])
        scan = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default=host): str,
                    vol.Required(CONF_SCAN_INTERVAL, default=scan): vol.All(
                        int, vol.Range(min=5, max=3600)
                    ),
                }
            ),
            errors=errors,
        )
