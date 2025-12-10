# 02WS Weather – Home Assistant Integration

Custom integration for pulling live Jerusalem weather data from https://www.02ws.co.il REST API.

## Install via HACS
1. Go to **HACS → Integrations → Custom repositories**  
2. Paste this repo URL  
3. Select **Integration**  
4. Search for “02WS Weather” and install

## Add to configuration.yaml

```yaml
sensor:
  - platform: 02ws