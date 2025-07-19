import sys
import atexit
import logging
import RPi.GPIO as GPIO
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os
import json

from temperature_service import TemperatureService


class Main:
    def __init__(self):
        self.configuration = self.read_configuration
        self.logger = self.setup_logging()

        self.logger.info(f"Application startup at: {datetime.now()}")
        self.logger.info("Using configuration path: appsettings.json")

        atexit.register(self.on_app_exit)
        sys.excepthook = self.log_unhandled_exception

        self.temperature_service = TemperatureService(self.configuration)

    @staticmethod
    def read_configuration():
        with open('appsettings.json', 'r') as f:
            return json.load(f)

    def on_app_exit(self):
        self.logger.info(f"Closing reader app at: {datetime.now()}")
        GPIO.cleanup()

    def log_unhandled_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self.logger.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

    def start(self):
        self.logger.info(f"Starting monitoring CPU temperature at: {datetime.now()}")
        self.temperature_service.start_monitoring()

    def setup_logging(self):
        log_dir = self.configuration.get('Logging', {}).get('DirectoryPath', './logs')
        days_to_keep = self.configuration.get('Logging', {}).get('MaxDays', 90)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_path = os.path.join(log_dir, 'readerLog.log')

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        file_handler = TimedRotatingFileHandler(
            log_path, when="S", interval=1, backupCount=days_to_keep, encoding='utf-8'
        )

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        file_handler.suffix = "%Y%m%d.log"
        file_handler.namer = lambda name: name.replace(".log.", "_")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger


if __name__ == '__main__':
    Main().start()
