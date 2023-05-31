import logging
import random
import time
from typing import Tuple

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

logging.basicConfig(filename='/var/log/en-expert-modbus-updater.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

interval_seconds = 120  # 2 mins for start
register_offset = 8  # we use 2 * 32 bit, so we have another 2 available
host = "localhost"


def start_service():
    while True:
        try:
            data = get_data()
            update_modbus(data)
        except Exception as e:
            logging.error(e)
        time.sleep(interval_seconds)


def get_data() -> list[Tuple]:
    # NOTE: If len(tuple) > 4 the register offset has to be increased.
    return generate_stub_data()


def generate_stub_data() -> list[Tuple]:
    length = 20

    stub_list = []

    for i in range(length):
        stub_list.append((random.uniform(0.0, 1000.0), random.uniform(0.0, 1000.0)))

    return stub_list


def update_modbus(data: list[Tuple]) -> None:
    client = ModbusClient(host)
    try:
        if not client.connect():
            raise ConnectionError("Cannot connect to modbus server on %s", host)
        for index, single_tuple in enumerate(data):
            address = index * register_offset
            for value in single_tuple:
                write_float_to_modbus(client=client, starting_address=address, value=value)
                address += 2  # 32 bit float uses 2 16-bit registers
    except Exception as err:
        logging.error("Cannot upload data to modbus server: %s", err)
    finally:
        client.close()


def write_float_to_modbus(client: ModbusClient, starting_address: int, value: float):
    """
    This function writes OVER the selected register.
    :param client:
    :param starting_address:
    :param value:
    :return:
    """
    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
    builder.add_32bit_float(value)
    registers = builder.to_registers()
    client.write_registers(starting_address, registers)


if __name__ == "__main__":
    logging.info("Starting Updater Service...")
    start_service()
