from threading import Thread
import time
from datetime import datetime
from pycomm3 import LogixDriver, SLCDriver
import pyodbc

from model import BatchEventData


class ReactorStart(Thread):

    def __init__(self, reactor_id, down_time_tag,reactor_name, tag_value_tag,bit_tag_label,tag_label,device_IP,device_id):
        super().__init__()
        self.start_bit = bit_tag_label+".StartCmd"
        self.running = bit_tag_label + ".Running"
        self.rector= reactor_name
        self.batch_number_tag = tag_label+".BatchHeader.BatchNumber"
        self.end_time_tag = tag_label+".BatchHeader.BatchEndTime"
        self.product_name_tag = tag_label+".BatchHeader.ProductName"
        self.tag_value_tag=tag_value_tag
        self.start_time_tag = tag_label+".BatchHeader.BatchStartTime"
        self.reactor_name_tag=tag_label+".BatchHeader.UnitName"

        self.ip=device_IP
        self.device_id=device_id

    def dateFormate(self, string_date):
        datedata = string_date.split("/")
        timedata = datedata[3].split(":")
        datetime2 = datetime(int(datedata[2]), int(datedata[1]), int(datedata[0]), int(timedata[0]), int(timedata[1]),
                             int(timedata[2]))
        return datetime2

    def startBit(self):
        while True:
            # try:
            # print("ip",self.ip)
            with LogixDriver(self.ip) as plc:
                print("start bit")
                print(self.running)
                data = plc.read(self.running)
                print("StartData",data)
                if (data[1] == True):
                    while True:
                        if (data[1] == False):
                            break
                        print("data true bit")
                        tag_value = plc.read(self.tag_value_tag)
                        BatchNumber=plc.read(self.batch_number_tag)
                        reactorName = plc.read(self.reactor_name_tag)
                        now = datetime.now()
                        print(now)
                        print(tag_value[1])
                        print(reactorName[1])
                        BatchEventData().insert(now,tag_value[1],reactorName[1],self.device_id)
                        print("tag_value", tag_value)

                        time.sleep(60)
            # except:
            #     print("except")
                # self.start_bit()

            #time.sleep(60)

    def run(self) -> None:

        self.startBit()
