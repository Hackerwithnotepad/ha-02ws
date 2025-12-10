"""02WS Weather integration."""
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "02ws"

async def async_setup(hass, config):
    _LOGGER.info("02WS integration loaded")
    return True
