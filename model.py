from database import Database
import datetime
import math

column_compare = {
    'EQUAL_TO': '=',
    'GREATER_THAN': '>',
    'GREATER_THAN_OR_EQUAL_TO': '>=',
    'LESSER_THAN': '<',
    'LESSER_THAN_OR_EQUAL_TO': '<='
}


class BatchModel:
    BATCH_TABLE = 'BatchReportData'

    def __init__(self):
       # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error



    def find_by_batch_id(self, batch_number):
        query_columns_dict = {
            'device_id': (column_compare['EQUAL_TO'], batch_number)
        }
        result = self._db.get_single_data(BatchModel.BATCH_TABLE, query_columns_dict)
        return result

    def find_by_batch_id_and_unitname(self, BatchNumber, UnitName):
        query_columns_dict = {
            'BatchNumber': (column_compare['EQUAL_TO'], BatchNumber),
            'UnitName': (column_compare['EQUAL_TO'], UnitName),


        }
        result = self._db.get_single_data(BatchModel.BATCH_TABLE, query_columns_dict)
        return result

    def insert(self, BatchStartTime,batchEndTime, ProductName,BatchNumber,UnitName, DeviceId):
        self.latest_error = ''
        # result = self.find_by_batch_id(BatchNumber)
        #
        # if (result):
        #     self.latest_error = f'Device id {BatchNumber} already exists!'
        #     return -1

        query_columns_dict = {
            'BatchStartTime': BatchStartTime,
            'BatchEndTime': batchEndTime,
            'ProductName': ProductName,
            'BatchNumber': BatchNumber,
            'UnitName': UnitName,
            'DownTime': '',
            'DeviceId':DeviceId
        }
        print("query_columns_dict",query_columns_dict)
        row_count = self._db.insert_single_data(BatchModel.BATCH_TABLE, query_columns_dict)
        return row_count

class ReportModel:
    REPORT_TABLE = 'BatchPhaseData'

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_by_batch_id(self, batch_number):
        query_columns_dict = {
            'device_id': (column_compare['EQUAL_TO'], batch_number)
        }
        result = self._db.get_single_data(ReportModel.REPORT_TABLE, query_columns_dict)
        return result

    def insert(self, BatchNumber, PhaseName, PhaseStartTime,PhaseEndTime,Setpoint,Actual,BatchReactorName,DeviceId):
        self.latest_error = ''
        # result = self.find_by_batch_id(BatchNumber)
        #
        # if (result):
        #     self.latest_error = f'Device id {BatchNumber} already exists!'
        #     return -1

        query_columns_dict = {
            'BatchNumber': BatchNumber,
            'PhaseName': PhaseName,
            'PhaseStartTime': PhaseStartTime,
            'PhaseEndTime': PhaseEndTime,
            'Setpoint':Setpoint,
            'Actual':Actual,
            'BatchReactorName':BatchReactorName,
            'DeviceId':DeviceId

        }

        row_count = self._db.insert_single_data(ReportModel.REPORT_TABLE, query_columns_dict)
        return row_count

class PhaseBitOfReactor:
    PhaseBitOfReactor_TABLE = 'phase_bit_of_reactor'

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_by_reactor_id(self, reactor_number):
        query_columns_dict = {
            'reactor_id': (column_compare['EQUAL_TO'], reactor_number)
        }
        result = self._db.get_single_data(PhaseBitOfReactor.PhaseBitOfReactor_TABLE, query_columns_dict)
        return result

class BatchReport:
    REPORT_TABLE = 'batch_report'

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_by_all_batch(self):

        result = self._db.get_multiple_data(BatchReport.REPORT_TABLE, None)
        return result


class DeviceModel:
    DEVICE_TABLE = 'device'

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_all_device(self):
        result = self._db.get_multiple_data(DeviceModel.DEVICE_TABLE, None)
        return result
    def find_device_by_id(self,device_id):
        query_columns_dict = {
            'id': (column_compare['EQUAL_TO'], device_id)
        }
        result = self._db.get_single_data(DeviceModel.DEVICE_TABLE, query_columns_dict)
        return result


class ReactorModel:
    REACTOR_TABLE = 'reactor_batch_report'

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_by_reactoreData(self,batch_id):
        query_columns_dict = {
            'batch_id': (column_compare['EQUAL_TO'], batch_id)
        }
        result = self._db.get_multiple_data(ReactorModel.REACTOR_TABLE, query_columns_dict)
        return result

class TagModel:
    TAG_TABLE = 'tag'

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_all_tag(self):
        result = self._db.get_multiple_data(TagModel.TAG_TABLE, None)
        return result


class FloatModel:
    FLOAT_TABLE = "float_table2"

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_by_batch_id(self, batch_number):
        query_columns_dict = {
            'device_id': (column_compare['EQUAL_TO'], batch_number)
        }
        result = self._db.get_single_data(FloatModel.FLOAT_TABLE, query_columns_dict)
        return result

    def insert(self, date_time, tag_id, value):
        self.latest_error = ''

        query_columns_dict = {
            'date_time': date_time,
            'tag_id': tag_id,
            'value': value,
        }

        row_count = self._db.insert_single_data(FloatModel.FLOAT_TABLE, query_columns_dict)
        return row_count

class AlertModel:
    ALERT_TABLE="alert"

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_all_alert(self):
        result = self._db.get_multiple_data(AlertModel.ALERT_TABLE, None)
        return result

class DeviationModel:
    DEVIATION_TABLE="deviation_table"

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_by_batch_id(self, batch_number):
        query_columns_dict = {
            'device_id': (column_compare['EQUAL_TO'], batch_number)
        }
        result = self._db.get_single_data(FloatModel.FLOAT_TABLE, query_columns_dict)
        return result

    def insert(self, date_time, alert_name, tag_index, tag_name, status, min_max, value, plc_id):
        self.latest_error = ''

        query_columns_dict = {
            'date_time': date_time,
            'alert_name': alert_name,
            'tag_index': tag_index,
            'tag_name':tag_name,
            'status':status,
            'min_max':min_max,
            'value':value,
            'plc_id':plc_id
        }

        row_count = self._db.insert_single_data(FloatModel.FLOAT_TABLE, query_columns_dict)
        return row_count

class BatchEventData:
    BATCHEVENTDATA_TABLE = "BatchEventData"

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error



    def insert(self, DateAndTime, Value,BatchReactorName,DeviceId):
        self.latest_error = ''

        query_columns_dict = {
            'DateAndTime': DateAndTime,
            'Value': Value,
            'BatchReactorName':BatchReactorName,
            'DeviceId':DeviceId
        }

        row_count = self._db.insert_single_data(BatchEventData.BATCHEVENTDATA_TABLE, query_columns_dict)
        return row_count



