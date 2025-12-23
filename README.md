# 02WS Weather — Home Assistant Integration

Custom integration for pulling live Jerusalem weather data from [02WS](https://www.02ws.co.il) (JeruSky / ירוש־מים) REST API.

This integration exposes the 02WS "now" API fields as individual Home Assistant sensors.

## About

- **Domain**: `o2ws` (note: **o**2ws, not 02ws — used internally by Home Assistant)  
- **Display Name**: "02WS Weather" (shown in UI)  
- **Update Interval**: 5 minutes  
- **Platform**: Sensor  

## Installation via HACS

1. Ensure the repository is public.  
2. Go to **HACS → Integrations → Custom repositories**  
3. Paste this repo URL and select **Integration**  
4. Search for **02WS Weather** and install  
5. Restart Home Assistant  

## Add to `configuration.yaml` (optional)

```yaml
sensor:
  - platform: o2ws