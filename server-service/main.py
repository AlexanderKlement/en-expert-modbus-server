import logging
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.server.sync import StartTcpServer

logging.basicConfig(filename='/var/log/en-expert-modbus-server.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_VALUE = 0
START_ADDRESS = 0
AMOUNT_REGISTERS = 200


def start_server():
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(START_ADDRESS, [DEFAULT_VALUE] * AMOUNT_REGISTERS))
    context = ModbusServerContext(slaves=store, single=True)

    StartTcpServer(context)


if __name__ == "__main__":
    logging.info("Starting Modbus Server/Slave...")
    start_server()
