import logging
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.server.async_io import StartTcpServer


logging.basicConfig(filename='/var/log/en-expert-modbus-server.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

default_value = 0
start_address = 0
amount_registers = 100


def start_server():
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(start_address, [default_value] * amount_registers))
    context = ModbusServerContext(slaves=store, single=True)

    StartTcpServer(context)


if __name__ == "__main__":
    logging.info("Starting Modbus Server/Slave...")
    start_server()
