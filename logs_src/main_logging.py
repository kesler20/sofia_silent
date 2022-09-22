import logging
import os

logger_name = os.path.basename(__file__)
logger_name = logger_name[:logger_name.find('_logging.py')]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(f'{logger_name} logger')

_handler = logging.FileHandler(os.path.join(
    os.path.dirname(__file__), f'{logger_name}_logs.log'))
_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')

_handler.setFormatter(formatter)

logger.addHandler(_handler)
