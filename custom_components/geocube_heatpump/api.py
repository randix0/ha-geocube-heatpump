"""Minimal client for the Carel pCOWeb getvar/setvar CSV interface."""
from __future__ import annotations

import csv
import io

import aiohttp
from yarl import URL

TIMEOUT = aiohttp.ClientTimeout(total=10)


class CarelApi:
    def __init__(self, session: aiohttp.ClientSession, host: str) -> None:
        self._session = session
        self.host = host

    async def get_vars(self, names: list[str]) -> dict[str, bool | float | str]:
        query = "&".join(f"name={n}" for n in names)
        url = URL(f"http://{self.host}/getvar.csv?{query}", encoded=True)
        async with self._session.get(url, timeout=TIMEOUT) as resp:
            resp.raise_for_status()
            text = await resp.text()

        result: dict[str, bool | float | str] = {}
        for row in csv.DictReader(io.StringIO(text)):
            name, vtype, val = row.get("name"), (row.get("type") or "").upper(), row.get("val")
            if not name or val is None:
                continue
            try:
                if vtype == "BOOL":
                    result[name] = val.strip().lower() in ("1", "true")
                elif vtype in ("REAL", "INT", "UINT", "DINT", "FLOAT"):
                    result[name] = float(val)
                else:
                    result[name] = val
            except ValueError:
                continue
        return result

    async def set_var(self, name: str, value: bool | int | float) -> None:
        if isinstance(value, bool):
            value = int(value)
        url = URL(f"http://{self.host}/setvar.csv?{name}={value}", encoded=True)
        async with self._session.get(url, timeout=TIMEOUT) as resp:
            resp.raise_for_status()
