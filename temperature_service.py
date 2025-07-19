import time
from enum import Enum
import RPi.GPIO as GPIO


class Fan(Enum):
    ON = 1
    OFF = 0


class TemperatureService:
    def __init__(self, configuration, logger):
        self.logger = logger
        self.configuration = configuration
        self.temperature_configuration = configuration['TemperatureConfiguration']

    @staticmethod
    def get_temperature():
        return 0

    def change_fan_state(self, state: Fan):
        pass

    def start_monitoring(self):
        while True:
            current_temperature = self.get_temperature()
            time.sleep(self.configuration['SecondDelayBetweenReads'])
