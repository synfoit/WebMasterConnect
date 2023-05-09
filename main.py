# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime

from pycomm3 import LogixDriver

from batch_data import DatabaseModel
from compexlogicPLC import Rockwell
from modbusConnector import ModbusConnector
from model import BatchModel, ReportModel
from simensePLC import Siemens


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    mo=ModbusConnector()
    mo.ModbusTCP()
    # dm = DatabaseModel()
    # data = dm.getReactorData()

    # rl=Rockwell()
    # rl.start()
    # sl=Siemens()
    # sl.start()



    # ReportModel().insert(batchNumber[1], phaseName[1], phaseStarttime, phaseEndtime, setPoint[1], actual[1],
    #                      reactorName[1], self.device_id)

