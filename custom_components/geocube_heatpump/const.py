"""Constants for the Carel heat pump integration."""
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import UnitOfTemperature

DOMAIN = "geocube_heatpump"
CONF_HOST = "host"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_HOST = "10.0.1.201"
DEFAULT_SCAN_INTERVAL = 30  # seconds

# ---------------------------------------------------------------------------
# Імена змінних контролера. Повний список: http://<IP>/getvar.csv
# ---------------------------------------------------------------------------
VAR_POWER = "OnOffUnitMng.KeybOnOff"

# key (ім'я змінної), назва, одиниці
SENSORS = [
    ("Outside_Air_Temperature", "Температура зовні", UnitOfTemperature.CELSIUS, "temperature"),
    ("Outlet_Water_Temp", "Теплоносій на виході", UnitOfTemperature.CELSIUS, "temperature"),
    ("Inlet_Water_Temp", "Теплоносій на вході", UnitOfTemperature.CELSIUS, "temperature"),
    ("Ground_Water_Temp", "Температура води у свердловині", UnitOfTemperature.CELSIUS, "temperature"),
    ("Room_Temp", "Температура кімнатна", UnitOfTemperature.CELSIUS, "temperature"),
]

# key, назва, device_class
BINARY_SENSORS = [
    ("Outputs.DO_3", "Нагрівач", BinarySensorDeviceClass.RUNNING),
    ("GlbAlrm", "Помилки", BinarySensorDeviceClass.PROBLEM),
]

# key, назва, min, max, step
NUMBERS = [
    ("Control.fixed_set_point", "Задана температура теплоносія", 10, 65, 0.5),
    ("Control.Room_Tmp_Set_Point", "Задана температура кімнатна", 10, 30, 0.5),
]

# Старі імена змінних -> нові: зберігає entity_id та історію наявних сутностей.
RENAMED_VARS = {
    "OutATmp": "Outside_Air_Temperature",
    "OutWTmp": "Outlet_Water_Temp",
    "RetWTmp": "Inlet_Water_Temp",
    "RoomTmp": "Room_Temp",
    "alm_critical": "GlbAlrm",
    "OutWTmp_SP": "Control.fixed_set_point",
    "RoomTmp_SP": "Control.Room_Tmp_Set_Point",
}
# Змінні, яких немає на контролері: їхні сутності видаляються.
REMOVED_VARS = {"PID_signal"}

ALL_VARS = (
    [VAR_POWER]
    + [s[0] for s in SENSORS]
    + [b[0] for b in BINARY_SENSORS]
    + [n[0] for n in NUMBERS]
)
