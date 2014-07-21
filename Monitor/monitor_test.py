import logging
import time
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("test")

logger.warn("Starting up")

while True:
  logger.info("Info message")
  logger.warn("Warning message")
  logger.error("Error message")
  time.sleep(2.0)

