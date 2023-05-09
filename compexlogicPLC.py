from threading import Thread
import pycomm3
import pyodbc
import time
from datetime import datetime
import pandas as pd

from model import DeviceModel, TagModel, FloatModel, AlertModel, DeviationModel

starttime = time.time()
from pycomm3 import LogixDriver

class Rockwell(Thread):

    def __init__(self):
        super().__init__()
        self.conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0I611GM\SQLEXPRESS;'
                              'Database=NewWeb1;'
                              'UID=sa;'
                              'PWD=Servilink@123;')


    def get_plcData(self):

        try:

            while True:
                deviceList = DeviceModel().find_all_device()
                for i in deviceList:
                    print(i)
                    if (i[6] == 'CL'):
                        tagList = TagModel().find_all_tag()


                        now = datetime.now()
                        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

                        for j in tagList:
                            print(j)
                            if (i[0] == j[2] and j[3] == True and j[6] == 'Auto'):

                                cursor1 = self.conn.cursor()
                                M = j[4]
                                index = j[0]

                                try:
                                    with LogixDriver(i[4]) as plc:
                                        data = plc.read(M)
                                        val = "%.2f" % round(data[1], 2)
                                        print(val)

                                        FloatModel().insert(now, index, val)

                                        cursor5 = self.conn.cursor()
                                        cursor5.execute(f"UPDATE device SET plc_status ='TRUE' Where id ={i[0]}")
                                        cursor5.commit()
                                except:
                                    cursor6 = self.conn.cursor()
                                    cursor6.execute(f"UPDATE device SET plc_status ='FALSE' Where id ={i[0]}")
                                    cursor6.commit()

                        alertList = AlertModel().find_all_alert()

                        for p in alertList:

                            if (i[0] == p[5] and p[6] == True):

                                cursor4 = self.conn.cursor()
                                M = p[7]
                                index = p[7]
                                print(i[3])
                                with LogixDriver(i[3]) as plc:
                                    data = plc.read(M)

                                    # print(p[4])
                                    if (data[1] < p[4]):
                                        DeviationModel().insert(now, p[1], p[8], p[9], 1, 'LOW', data[1], p[5])

                                    if (data[1] > p[3]):
                                        print("no")
                                        DeviationModel().insert(now, p[1], p[8], p[9], 1, 'HIGH', data[1], p[5])
                time.sleep(60)

        except:

            self.get_plcData()

    def run(self) -> None:
        self.get_plcData()
        time.sleep(1)
