import logging
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.sync import StartTcpServer

logging.basicConfig(filename='/var/log/en-expert-modbus-server.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_VALUE = 0
START_ADDRESS = 0x0
AMOUNT_REGISTERS = 0x2000


def start_server():
    block = ModbusSequentialDataBlock(START_ADDRESS, [DEFAULT_VALUE] * AMOUNT_REGISTERS)
    store = ModbusSlaveContext(hr=block)
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '1.0'

    logging.info("Starting Modbus Server/Slave...")
    StartTcpServer(context, identity=identity)


if __name__ == "__main__":
    logging.info("Starting Modbus Server/Slave...")
    start_server()
