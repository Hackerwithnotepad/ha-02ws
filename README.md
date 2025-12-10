# ha-02ws — 02WS / JeruSky Home Assistant Integration

Exposes 02WS (JeruSky / ירוש־מים) "now" API fields as individual Home Assistant sensors.

## Install

1. Ensure repository is public.
2. Add repo to HACS → Integrations → Custom repositories → paste URL → select "Integration".
3. Install integration from HACS → Integrations, restart Home Assistant.

## Sensors exposed
- 02WS Temperature (°C)
- 02WS Temperature 2 (°C)
- 02WS Temperature 3 (°C)
- 02WS Humidity (%)
- 02WS Pressure (hPa)
- 02WS Wind Direction
- 02WS Wind Speed (km/h)
- 02WS Rain Rate (mm/h)
- 02WS Rain Chance (%)
- 02WS Solar Radiation (W/m²)
- 02WS Sunshine Hours (h)
- 02WS Rain Total (mm)
- 02WS Time

## API
This integration pulls data from: `https://www.02ws.co.il/api/now/0/1/C/1`
