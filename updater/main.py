import logging
import random
import requests
import time
from typing import List, Tuple
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import os

if os.name != 'nt':
    logging.basicConfig(filename='/var/log/en-expert-modbus-updater.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

INTERVAL_SECONDS = 10  # reduced to 10 mins, hope this is ok
REGISTER_SIZE = 2  # 32 bit
BLOCK_SIZE = 8
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
    # The URL you want to make a GET request to
    # This link will soon be ip regulated, therefore leaking this shouldn't be a problem
    url = "https://api2.en-expert.com/measurment/last_ekos_value/KWCD0hwIP52zJ3SvJR8lNGa21e6UP46OhbC8o9YrX1FBI7DFXbtSdsMdWpV3hhpy"

    # Make a GET request
    response = requests.get(url, headers={"accept": "application/json"}, timeout=INTERVAL_SECONDS)

    # Check that the request was successful
    if response.status_code == 200:
        # Parse the JSON response into a Python dictionary
        data = response.json()

        list_of_tuples = [(
            item["powerActual"],
            item["powerIntegral"],
            item["voltage"],
            item["frequency"],
            item["thdu"],
            item["peakVoltage"],
        ) for item in data]

        return list_of_tuples

    logging.error("Request failed with status code %s", response.status_code)
    return []


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
            raise ConnectionError("Cannot connect to modbus server on " + HOST)
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
