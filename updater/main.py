import logging
import random
import time
from typing import List, Tuple
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

logging.basicConfig(filename='/var/log/en-expert-modbus-updater.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

INTERVAL_SECONDS = 120  # 2 mins for start
REGISTER_SIZE = 2  # 32 bit
BLOCK_SIZE = 10
REGISTER_OFFSET = REGISTER_SIZE * BLOCK_SIZE  # we use 2 * 32 bit, so we have another 2 available
START = 0x1000
HOST = "localhost"


def start_service():
    # Just making sure the modbus server is available.
    time.sleep(2)
    while True:
        try:
            data = get_data()
            update_modbus(data)
        except Exception as err:
            logging.error(err)
        time.sleep(INTERVAL_SECONDS)


def get_data() -> List[Tuple]:
    # NOTE: If len(tuple) > 4 the register offset has to be increased.
    return generate_stub_data()


def generate_stub_data() -> List[Tuple]:
    length = 4

    stub_list = []

    for _ in range(length):
        stub_list.append(tuple(random.uniform(0.0, 1000.0) for _ in range(6)))

    return stub_list


def set_fixed_data(client: ModbusClient):
    write_float_to_modbus(client=client, starting_address=0x100, value=1)
    write_float_to_modbus(client=client, starting_address=0x102, value=100)


def update_modbus(data: List[Tuple]) -> None:
    client = ModbusClient(HOST, port=1502)
    try:
        if not client.connect():
            raise ConnectionError("Cannot connect to modbus server on {}".format(HOST))
        set_fixed_data(client=client)
        for index, single_tuple in enumerate(data):
            address = START + (index * REGISTER_OFFSET)
            for value in single_tuple:
                write_float_to_modbus(client=client, starting_address=address, value=value)
                address += REGISTER_SIZE  # 32 bit float uses 2 16-bit registers
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
