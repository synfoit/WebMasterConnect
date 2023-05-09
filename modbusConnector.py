from pyModbusTCP.client import ModbusClient # Modbus TCP Client
import time
import pyodbc
import struct
from datetime import datetime
# TCP auto connect on modbus request, close after it
from model import DeviceModel, TagModel


class ModbusConnector:
   def __init__(self):
      super().__init__()
      self.conn = pyodbc.connect('Driver={SQL Server};'
                                 'Server=DESKTOP-0I611GM\SQLEXPRESS;'
                                 'Database=NewWeb1;'
                                 'UID=sa;'
                                 'PWD=Servilink@123;')
   def ModbusTCP(self):

      try:

         while True:
            deviceList = DeviceModel().find_all_device()
            for i in deviceList:

               if (i[6] == 'modbus'):
                  tagList = TagModel().find_all_tag()

                  now = datetime.now()
                  dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

                  for j in tagList:

                     if (i[0] == j[2] and j[3] == True and j[6] == 'Auto'):

                        cursor1 = self.conn.cursor()
                        M = j[4]
                        index = j[0]
                        print(M)
                        try:
                           ModbusBMS = ModbusClient(host=i[4], port=i[12], unit_id=i[13], auto_open=True, auto_close=True)

                           print(hex(j[4]))
                           hexaadress=hex(j[4]-1)
                           data=ModbusBMS.read_input_registers(hexaadress,j[8])
                           # data = ModbusBMS.read_input_registers(30054, 2)
                           print("dttt",data)

                           if(j[7]==0):
                              packed_string = struct.pack("HH", data[0], data[1])
                              unpacked_float = struct.unpack("f", packed_string)[0]
                              print(unpacked_float)
                           elif(j[7]==1):
                              packed_string = struct.pack("HH", data[1], data[0])
                              unpacked_float = struct.unpack("f", packed_string)[0]
                              print(unpacked_float)
                        except:
                           print("data")
      except:
         print("except")
