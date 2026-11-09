"""Constants for the Carel heat pump integration."""
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import PERCENTAGE, UnitOfTemperature

DOMAIN = "geocube_heatpump"
CONF_HOST = "host"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_HOST = "10.0.1.201"
DEFAULT_SCAN_INTERVAL = 30  # seconds

# ---------------------------------------------------------------------------
# Імена змінних контролера. Якщо у вашому контролері вони відрізняються
# (напр. Outside_Air_Temperature замість OutATmp) - змініть тут.
# ---------------------------------------------------------------------------
VAR_POWER = "OnOffUnitMng.KeybOnOff"

# key (ім'я змінної), назва, одиниці
SENSORS = [
    ("OutATmp", "Температура зовні", UnitOfTemperature.CELSIUS, "temperature"),
    ("OutWTmp", "Теплоносій на виході", UnitOfTemperature.CELSIUS, "temperature"),
    ("RetWTmp", "Теплоносій на вході", UnitOfTemperature.CELSIUS, "temperature"),
    ("Ground_Water_Temp", "Температура води у свердловині", UnitOfTemperature.CELSIUS, "temperature"),
    ("RoomTmp", "Температура кімнатна", UnitOfTemperature.CELSIUS, "temperature"),
    ("PID_signal", "Сигнал PID", PERCENTAGE, None),
]

# key, назва, device_class
BINARY_SENSORS = [
    ("Outputs.DO_3", "Нагрівач", BinarySensorDeviceClass.RUNNING),
    ("alm_critical", "Помилки", BinarySensorDeviceClass.PROBLEM),
]

# key, назва, min, max, step
NUMBERS = [
    ("OutWTmp_SP", "Задана температура теплоносія", 10, 65, 0.5),
    ("RoomTmp_SP", "Задана температура кімнатна", 10, 30, 0.5),
]

ALL_VARS = (
    [VAR_POWER]
    + [s[0] for s in SENSORS]
    + [b[0] for b in BINARY_SENSORS]
    + [n[0] for n in NUMBERS]
)
