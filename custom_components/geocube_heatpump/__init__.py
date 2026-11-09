"""Carel heat pump integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import CarelApi
from .const import (
    CONF_HOST,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    REMOVED_VARS,
    RENAMED_VARS,
)
from .coordinator import CarelCoordinator

PLATFORMS = ["sensor", "binary_sensor", "switch", "number"]


@callback
def _migrate_entities(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Move registry entries created with outdated variable names."""
    registry = er.async_get(hass)
    prefix = f"{entry.entry_id}_"
    for reg_entry in er.async_entries_for_config_entry(registry, entry.entry_id):
        key = reg_entry.unique_id.removeprefix(prefix)
        if key in REMOVED_VARS:
            registry.async_remove(reg_entry.entity_id)
        elif key in RENAMED_VARS:
            registry.async_update_entity(
                reg_entry.entity_id, new_unique_id=f"{prefix}{RENAMED_VARS[key]}"
            )


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _migrate_entities(hass, entry)
    host = entry.options.get(CONF_HOST, entry.data[CONF_HOST])
    scan = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    api = CarelApi(async_get_clientsession(hass), host)
    coordinator = CarelCoordinator(hass, api, scan)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    entry.async_on_unload(entry.add_update_listener(_reload))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def _reload(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return ok
