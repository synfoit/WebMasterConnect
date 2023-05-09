import pyodbc
import pandas as pd

from ReactorEndbit import ReactorEndBit
from model import BatchReport, ReactorModel, DeviceModel
from read_for_reactor import ReactorStart


class DatabaseModel:

    def getReactorData(self):
        batchlist = BatchReport().find_by_all_batch()
        #print("batchlist",batchlist)
        for i in batchlist:

            batch_id = i[0]
            batch_report_name = i[1]
            bit_tag_label = i[2]
            create_by = i[3]
            device_id = i[4]
            status = i[5]
            tag_label = i[6]
            deviceData=DeviceModel().find_device_by_id(device_id)
            device_IP=deviceData[4]
            # print(deviceData[4])
            results = ReactorModel().find_by_reactoreData(i[0])
            #print("result",results)
            for idx, j in enumerate(results):
                # print(idx, j)
                reactor_id=j[0]
                down_time_tag=j[2]
                reactor_index=j[3]
                reactor_name=j[4]
                tag_value_tag=j[5]

                rt = ReactorStart(reactor_id, down_time_tag,reactor_name, tag_value_tag,bit_tag_label+"["+str(reactor_index)+"]",tag_label+"["+str(reactor_index)+"]",device_IP,device_id)
                rt.start()

                et=ReactorEndBit(reactor_id, down_time_tag,reactor_name, tag_value_tag,bit_tag_label+"["+str(reactor_index)+"]",tag_label+"["+str(reactor_index)+"]",device_IP,reactor_index,device_id)
                et.start()











