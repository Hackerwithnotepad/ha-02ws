import aiohttp
import async_timeout
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorEntity
from homeassistant.util import Throttle
from .const import BASE_URL

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)

SENSOR_MAP = {
    "temp": "Temperature",
    "temp2": "Temperature 2",
    "temp3": "Temperature 3",
    "hum": "Humidity",
    "pressure": "Pressure",
    "winddir": "Wind Direction",
    "windspd": "Wind Speed",
    "rainrate": "Rain Rate",
    "rainchance": "Rain Chance",
    "solarradiation": "Solar Radiation",
    "sunshinehours": "Sunshine Hours",
    "rain": "Rain Total"
}

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    data = WeatherData(hass)
    await data.update()

    sensors = []
    for key, name in SENSOR_MAP.items():
        sensors.append(WeatherSensor(data, key, name))

    add_entities(sensors, True)

class WeatherData:
    def __init__(self, hass):
        self.hass = hass
        self.data = {}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def update(self):
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                async with session.get(BASE_URL) as resp:
                    self.data = await resp.json()

class WeatherSensor(SensorEntity):
    def __init__(self, data, key, name):
        self.data = data
        self.key = key
        self._name = name

    @property
    def name(self):
        return f"02WS {self._name}"

    @property
    def state(self):
        return self.data.data.get(self.key)

    async def async_update(self):
        await self.data.update()