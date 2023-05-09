from threading import Thread
import pyodbc
import snap7
from snap7.exceptions import Snap7Exception
from snap7.util import *
from snap7.types import *
import time
from model import DeviceModel, TagModel, FloatModel, AlertModel, DeviationModel


class Siemens(Thread):

    def __init__(self):
        super().__init__()
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                   'Server=DESKTOP-0I611GM\SQLEXPRESS;'
                                   'Database=NewWeb1;'
                                   'UID=sa;'
                                   'PWD=Servilink@123;')

    def ReadMemory(self, plc, byte, bit, datatype):  # define read memory function
        result = plc.read_area(snap7.types.Areas.MK, 0, byte, datatype)
        if datatype == S7WLBit:
            return get_bool(result, 0, 1)
        elif datatype == S7WLByte or datatype == S7WLWord:
            return get_int(result, 0)
        elif datatype == S7WLReal:
            return get_real(result, 0)
        elif datatype == S7WLDWord:
            return get_dword(result, 0)
        elif datatype == S7WLInt:
            return get_int(result, 0)
        else:
            return None

    def sleeptime(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM device')

    def getSimensPlcData(self):
        try:
            plc = snap7.client.Client()
            while True:
                deviceList = DeviceModel().find_all_device()

                for i in deviceList:

                    if (i[5] == 'S7'):
                        IP = i[3]
                        RACK = 0
                        SLOT = 1
                        if plc.get_connected() == False:
                            try:
                                plc.connect(IP, RACK, SLOT)  # ('IP-address', rack, slot)

                                time.sleep(0.2)
                            except Snap7Exception as e:
                                continue
                        else:
                            tagList = TagModel().find_all_tag()

                            from datetime import datetime
                            now = datetime.now()
                            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

                            for j in tagList:
                                if (i[0] == j[2] and j[3] == True):
                                    state = plc.get_cpu_state()  # read plc state run/stop/error
                                    # print state plc
                                    index = j[0]

                                    if (j[1] == 'Float'):
                                        readreal = self.ReadMemory(self, plc, int(j[4]), 0, S7WLReal)
                                        FloatModel().insert(now, index, readreal)  # read md15

                                    if (j[1] == 'Integer'):
                                        readword = self.ReadMemory(self, plc, int(j[4]), 0, S7WLInt)  # read mw10
                                        FloatModel().insert(now, index, readword)

                            alertList = AlertModel().find_all_alert()

                            for p in alertList:

                                if (i[0] == p[8] and p[4] == True):

                                    M = p[7]
                                    index = p[7]

                                    state = plc.get_cpu_state()  # read plc state run/stop/error
                                    # print state plc

                                    if (p[9] == 'Float'):
                                        readreal = self.ReadMemory(self, plc, int(p[7]), 0, S7WLReal)  # read md15
                                        if (readreal < p[3]):
                                            DeviationModel().insert(now, p[1], p[5], p[5], 1, 'LOW', readreal, p[8])

                                        if (readreal > p[2]):
                                            DeviationModel().insert(now, p[1], p[5], p[5], 1, 'LOW', readreal, p[8])

                                    if (p[9] == 'Integer'):
                                        readreal = self.ReadMemory(self, plc, int(p[7]), 0, S7WLInt)  # read md15
                                        if (readreal < p[3]):
                                            DeviationModel().insert(now, p[1], p[5], p[5], 1, 'LOW', readreal, p[8])

                                        if (readreal > p[2]):
                                            DeviationModel().insert(now, p[1], p[5], p[5], 1, 'LOW', readreal, p[8])

                time.sleep(50)

        except:
            self.getSimensPlcData()

    def run(self) -> None:
        self.getSimensPlcData()
        time.sleep(1)