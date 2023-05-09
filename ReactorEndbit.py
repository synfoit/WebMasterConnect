from threading import Thread
import time
from datetime import datetime
from pycomm3 import LogixDriver, SLCDriver
import pyodbc

from model import ReportModel, PhaseBitOfReactor, BatchModel


class ReactorEndBit(Thread):

    def __init__(self, reactor_id, down_time_tag,reactor_name, tag_value_tag,bit_tag_label,tag_label,device_IP,reactor_index,device_id):
        super().__init__()
        self.end_bit_tag = bit_tag_label + ".Complete"
        self.rector = reactor_name
        self.running = bit_tag_label + ".Running"
        self.batch_number_tag = tag_label + ".BatchHeader.BatchNumber"
        self.end_time_tag = tag_label + ".BatchHeader.BatchEndTime"
        self.product_name_tag = tag_label + ".BatchHeader.ProductName"
        self.phase_count_tag=bit_tag_label+".TotalSteps"
        self.start_time_tag = tag_label + ".BatchHeader.BatchStartTime"
        self.reactor_name_tag = tag_label + ".BatchHeader.UnitName"
        self.ip = device_IP
        self.down_time_tag=down_time_tag
        self.tag_label=tag_label
        self.device_id=device_id
        self.connection = pyodbc.connect('Driver={SQL Server};'
                                         'Server=DESKTOP-0I611GM\SQLEXPRESS;'
                                         'Database=NewWeb1;'
                                         'UID=sa;'
                                         'PWD=Servilink@123;')
        self.cursor = self.connection.cursor()

    def dateFormate(self,string_date):
        datedata = string_date.split("/")
        timedata = datedata[3].split(":")
        datetime2 = datetime(int(datedata[2]), int(datedata[1]), int(datedata[0]), int(timedata[0]), int(timedata[1]),
                     int(timedata[2]))

        return datetime2

    def endBit(self):
        # try:
        while True:
            # print("endbit")
            # print("ip", self.ip)
            with LogixDriver(self.ip) as plc:
                print("connection", plc.connected)
                data = plc.read(self.running)
                print("Enddata", data)
                if (data[1] == False):
                    batchNumber = plc.read(self.batch_number_tag)
                    reactorName = plc.read(self.reactor_name_tag)
                    productName = plc.read(self.product_name_tag)
                    start_time = plc.read(self.start_time_tag)
                    batchStratTime = self.dateFormate(str(start_time[1]))
                    phaseCount = plc.read(self.phase_count_tag)
                    end_time = plc.read(self.end_time_tag)
                    batchEndTime = self.dateFormate(str(end_time[1]))

                    countofbatch=BatchModel().find_by_batch_id_and_unitname(batchNumber[1],reactorName[1])

                    if(countofbatch==None):


                        BatchModel().insert(batchStratTime,batchEndTime, productName[1], batchNumber[1], reactorName[1],self.device_id)

                        for j in range(phaseCount[1]):
                            actual=plc.read(self.tag_label+".PhaseReport"+"["+str(j)+"]"+".PhaseData[0].Actual")
                            print("actual",actual[1])
                            print("actualtag", self.tag_label+".PhaseReport"+"["+str(j)+"]"+".PhaseData[0].Actual")
                            pe=plc.read(self.tag_label+".PhaseReport"+"["+str(j)+"]"+".PhaseHeader.EndTime")
                            #print("pe", pe)
                            phaseEndtime=self.dateFormate(pe[1])
                            #print("phaseEndtime", phaseEndtime)
                            setPoint=plc.read(self.tag_label+".PhaseReport"+"["+str(j)+"]"+".PhaseData[0].Setpoint")
                            print("setPoint", setPoint[1])
                            print("setPointtag", self.tag_label+".PhaseReport"+"["+str(j)+"]"+".PhaseData[0].Setpoint")

                            ps=plc.read(self.tag_label+".PhaseReport"+"["+str(j)+"]"+".PhaseHeader.StartTime")

                            phaseStarttime=self.dateFormate(ps[1])
                            #print("phaseStarttime", phaseStarttime)
                            phaseName=plc.read(self.tag_label+".PhaseReport"+"["+str(j)+"]"+".PhaseHeader.Name")
                            #print("phaseName",phaseName[1])
                            if(len(setPoint) !=0 or len(actual) !=0):
                                ReportModel().insert(batchNumber[1],phaseName[1],phaseStarttime,phaseEndtime,setPoint[1],actual[1],reactorName[1],self.device_id)


            time.sleep(1)
        # except:
        #     print("except")
            # self.endBit()
    def run(self) -> None:
        self.endBit()



