import logging
import time

logging.basicConfig(filename='/var/log/en-expert-modbus-service.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

interval_seconds = 10


def start_service():
    while True:
        try:
            data = do_database_stuff()
            update_modbus(data)
        except Exception as e:
            logging.error(e)
        time.sleep(interval_seconds)


def do_database_stuff() -> dict:
    return {}


def update_modbus(data: dict) -> None:
    pass


if __name__ == "__main__":
    logging.info("Starting Database Service...")
    start_service()
