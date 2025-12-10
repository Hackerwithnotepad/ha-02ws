import asyncio
import aiohttp
import async_timeout
import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from .const import API_URL, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=SCAN_INTERVAL_SECONDS)

SENSOR_MAP = {
    "time": {"name": "Time", "unit": None, "device_class": None, "icon": "mdi:clock"},
    "temp": {"name": "Temperature", "unit": "°C", "device_class": "temperature", "icon": "mdi:thermometer"},
    "temp2": {"name": "Temperature 2", "unit": "°C", "device_class": "temperature", "icon": "mdi:thermometer"},
    "temp3": {"name": "Temperature 3", "unit": "°C", "device_class": "temperature", "icon": "mdi:thermometer"},
    "hum": {"name": "Humidity", "unit": "%", "device_class": "humidity", "icon": "mdi:water-percent"},
    "pressure": {"name": "Pressure", "unit": "hPa", "device_class": "pressure", "icon": "mdi:gauge"},
    "winddir": {"name": "Wind Direction", "unit": None, "device_class": None, "icon": "mdi:compass"},
    "windspd": {"name": "Wind Speed", "unit": "km/h", "device_class": None, "icon": "mdi:weather-windy"},
    "rainrate": {"name": "Rain Rate", "unit": "mm/h", "device_class": None, "icon": "mdi:weather-rainy"},
    "rainchance": {"name": "Rain Chance", "unit": "%", "device_class": None, "icon": "mdi:weather-pouring"},
    "solarradiation": {"name": "Solar Radiation", "unit": "W/m²", "device_class": None, "icon": "mdi:weather-sunny"},
    "sunshinehours": {"name": "Sunshine Hours", "unit": "h", "device_class": None, "icon": "mdi:weather-sunny"},
    "rain": {"name": "Rain Total", "unit": "mm", "device_class": None, "icon": "mdi:weather-rainy"}
}


async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up 02WS sensors as individual entities."""
    data = WeatherData(hass)
    sensors = [WeatherSensor(data, key, info) for key, info in SENSOR_MAP.items()]
    add_entities(sensors, True)


class WeatherData:
    """Fetches data from 02WS API."""

    def __init__(self, hass):
        self.hass = hass
        self.data = {}
        self._session = None
        self._lock = asyncio.Lock()

    async def _get_session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Fetch new data from API (throttled)."""
        async with self._lock:
            try:
                session = await self._get_session()
                with async_timeout.timeout(10):
                    async with session.get(API_URL) as resp:
                        if resp.status != 200:
                            _LOGGER.warning("02WS API returned status %s", resp.status)
                            return
                        json_data = await resp.json()
                        # Ensure the data is a dict
                        if isinstance(json_data, dict):
                            self.data = json_data
                        else:
                            _LOGGER.warning("02WS API returned unexpected JSON: %s", type(json_data))
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                _LOGGER.exception("Error fetching 02WS data: %s", exc)


class WeatherSensor(SensorEntity):
    """Representation of a single 02WS sensor."""

    def __init__(self, data, key, info):
        self._data = data
        self._key = key
        self._attr_name = f"02WS {info.get('name')}"
        self._unit = info.get("unit")
        self._device_class = info.get("device_class")
        self._icon = info.get("icon")
        self._state = None

    @property
    def name(self):
        return self._attr_name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def device_class(self):
        return self._device_class

    @property
    def icon(self):
        return self._icon

    async def async_update(self):
        """Update state from the shared data object."""
        await self._data.async_update()
        value = self._data.data.get(self._key)
        # convert numeric-looking strings to numbers
        try:
            if value is None:
                self._state = None
            elif isinstance(value, (int, float)):
                self._state = value
            elif isinstance(value, str):
                # try int then float, otherwise keep string
                if value.isdigit():
                    self._state = int(value)
                else:
                    try:
                        self._state = float(value)
                    except ValueError:
                        self._state = value
            else:
                self._state = value
        except Exception:
            self._state = value
