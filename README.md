# Geocube Heat Pump для Home Assistant

Кастомна інтеграція Home Assistant для теплових насосів Geocube на контролері Carel (pCOWeb)
з вебінтерфейсом `getvar.csv` / `setvar.csv`. Працює локально, без хмари.

## Можливості

- Сенсори температур: зовнішня, теплоносій на виході/вході, вода у свердловині, кімнатна
- Сигнал PID
- Перемикач Вкл/викл теплового насоса
- Задані температури теплоносія та кімнатна (можна змінювати)
- Стан нагрівача та критичні помилки
- Налаштування через UI, IP-адреса та інтервал опитування змінюються без перезапуску

## Встановлення

### HACS (custom repository)

1. HACS → ⋮ → **Custom repositories**
2. Додайте URL цього репозиторію, категорія **Integration**
3. Встановіть **Geocube Heat Pump** і перезапустіть Home Assistant

### Вручну

Скопіюйте `custom_components/geocube_heatpump` у `config/custom_components/` і перезапустіть HA.

## Налаштування

*Налаштування → Пристрої та служби → Додати інтеграцію → Geocube Heat Pump*,
введіть IP-адресу контролера (наприклад `10.0.1.201`).

## Змінні контролера

Імена змінних задані в [`const.py`](custom_components/geocube_heatpump/const.py).
Якщо у вашому контролері вони відрізняються, відредагуйте списки
`SENSORS`, `BINARY_SENSORS` і `NUMBERS`.

Перегляд доступних змінних: `http://<IP>/getvar.csv`.

## Протокол

| Дія | Запит |
|---|---|
| Читання | `GET http://<IP>/getvar.csv?name=A&name=B` |
| Запис | `GET http://<IP>/setvar.csv?name=OnOffUnitMng.KeybOnOff=1` |

## Ліцензія

MIT
