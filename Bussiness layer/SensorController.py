################################################
## Project: ASS/NSS API 
## Author: David Michalica, Team 1
## Date: 2024
## 
## Documentation: https://bitbucket.org/dakel/node-zedo-rpc/src/master/API.md
## alternativni knihovny pro py: pyro4, xmlrpc.server, jsonrpcserver, zerorpc
#################################################

import socket
import threading
import time
import datetime
import json

class SensorController:

    methods =  {
        "GRFN": "generate_rec_folder_name",
        "CV": "compare_versions",
        "AMV": "assert_min_version",
        "CJ": "copy_json",
        "PJ": "print_json",
        "IJO": "is_json_object",
        "MJ": "merge_json",
        "IZD": "is_zdat_directory",
        "GS": "GetSensors",
        "GSS": "GetSystemStatus",
        "GST": "GetSystemTime",
        "GC": "GetConfiguration",
        "C": "Configure",
        "CLD": "ClearLiveData",
        "SR": "StartRecording",
        "PR": "PauseRecording",
        "StR": "StopRecording",
        "GRS": "GetRecordingState",
        "GAI": "GetAppInfo",
        "GAP": "GetActivePulsers",
        "APO": "AllPulsersOff",
        "PCS": "pulser_configs_same",
        "SP": "SetPulser",
        "ECR": "EnableContinuousRecording",
        "OFRBP": "OpenFileReaderByPath",
        "OFRBN": "OpenFileReaderByName",
        "SFRP": "SetFileReaderPath",
        "GFRI": "GetFileReaderInfo",
        "GFRD": "GetFileReaderData",
        "EFRD": "ExportFileReaderData",
        "EI": "ExportItems",
        "CGP": "CaptureGraphPictures",
        "WFRS": "WaitFileReaderScanned",
        "WI": "WaitItemsIdle",
        "GEJS": "GetExportJobStatus",
        "AEJ": "AbortExportJob",
        "WBJF": "WaitBackroundJobFinished",
        "EJPM": "ExportJobProgressMonitor",
        "GII": "GetItemInfo",
        "GSI": "GetSubItems"
    }
    
    def __init__(self, ip, port):
        self.IP_ADDR = ip
        self.PORT = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Connect(self):
        self.client_socket.connect((self.IP_ADDR, self.PORT))

    def Call(self, method, id, params = {}):
        # Vytvoření slovníku s hodnotami pro volání
        call_values = {
            'jsonrpc': '2.0', 
            'method': method, 
            'id': id,
            "params": params
        }

        # Převod slovníku na řetězec JSON
        json_string = json.dumps(call_values)

        # Převod řetězce JSON na bajty
        bytes_to_send = json_string.encode('utf-8')    

        # Odeslání bajtů přes socket
        self.client_socket.send(bytes_to_send)
        response = self.client_socket.recv(4096)  # Přečte až 4096 bajtů (můžete upravit podle potřeby)

        # Převod bajtů na řetězec
        response_string = response.decode('utf-8')   
        return response_string 


    def Generate_rec_folder_name(self, id, prefix:str, use_date:bool = True, use_m:bool = True, use_sec:bool = True, name_delimeter:str = '-', time_delimeter:str = '-', now:datetime = None):
        """
        Helper call to get date-time folder name

        :param prefix: str - Folder name prefix
        :param use_date: bool - Use date in the name, default true (optional, default true)
        :param use_hm: bool - Use time HH:MM in the name, default true (optional, default true)
        :param use_sec: bool - Use time HH:MM:SS in the name, default false (optional, default false)
        :param name_delimiter: str - Delimiter between prefix, date and time portions (optional, default '-')
        :param date_delimiter: str - Delimiter between year, month and day values (optional, default '-')
        :param time_delimiter: str - Delimiter between hour, minute and second values (optional, default '-')
        :param now: datetime.datetime - Time value to use. Uses current time when not specified (optional, default None)

        :return: str - Generated folder name
        """
        params = {
            "prefix": prefix,
            "use_date": use_date,
            "use_m": use_m,
            "use_sec": use_sec,
            "name_delimeter": name_delimeter
        }
        return self.Call(self.methods["GRFN"], id, params)

    def Compare_versions(self, id, ver_a:str, ver_b:str):
        """
        Compare version or build strings

        :param ver_a: str - Version A, format "X.Y", "X.Y.Z" or "X.Y.Z.BUILD" or just BUILD number
        :param ver_b: str - Version B, same format options as above

        :return: int - -1, 0, +1 as a traditional compare result
        """
        params = {
            "ver_a": ver_a,
            "ver_b": ver_b,
        }
        return self.Call("Compare_versions", id, params)

    def Assert_min_version(self, id, min_version:str, assert_time:str):
        """
        Make sure the ZDaemon app is at specific version or above

        :param min_version: Union[str, int] - Version A, format "X.Y", "X.Y.Z" or "X.Y.Z.BUILD" or just BUILD number
        :param assert_name: Any - Assert name

        :return: Any - This function throws an exception if lower version is detected
        """
        params = {
            "min_version": min_version,
            "assert_time": assert_time,
        }
        return self.Call("Assert_min_version", id, params)

    def Copy_json(self, id, obj:object):
        """
        Return a deep copy of given object using JSON stringify/parse methods

        :param obj: Any - Input object
        :return: Any - Cloned object
        """
        params = {
            "obj": obj,
        }
        return self.Call("Copy_json", id, params)

    def Print_json(self, id, obj:object):
        """
        Print formatted JSON object to console

        :param obj: Any - Input object
        :return: None
        """
        params = {
            "obj": obj,
        }
        return self.Call("Print_json", id, params)

    def Is_json_object(self, id, obj:object):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        params = {
            "obj": obj,
        }
        return self.Call("Is_json_object", id, params)

    def Merge_json(self, id, dest, src, overwrite_values:bool, overwrite_objects:bool):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        params = {
            "min_version": dest,
            "assert_time": src,
            "overwrite_values": overwrite_values,
            "overwrite_objects": overwrite_objects,
        }
        return self.Call("Merge_json", id, params)

    def Is_zdat_directory(self, id, path:str):
        """
        Determine if local path is a ZEDO data directory (zedodata.zdat file present)

        :param path: str - Source data directory or directories to open.
        :return: bool - Test result
        """ 
        params = {
            "path": path,
        }
        return self.Call("Is_zdat_directory", id, params)

    def GetSensors(self, id, verbosity:str = "all"):
        """
        ZEDO RPC call: Obtain array of sensor configurations

        :param verbosity: str - Required verbosity of output; examples: "min", "max", "gain|pulser", .. default is "all"
        :return: Promise - '.then' returns current configuration objects in required verbosity
        """
        params = {
            "verbosity": verbosity,
        }
        return self.Call("GetSensors", id, params)

    def GetSystemStatus(self, id):
        """
        ZEDO RPC call: Get system status overview, number of dead/alive units etc.

        :return: Promise - '.then' returns the response object
        """
        params = {}
        return self.Call("GetSystemStatus", id, params)

    def GetSystemTime(self, id):
        """
        ZEDO RPC call: Get system time in both hardware nanosecond time and in formatted local time

        :return: Promise - '.then' returns the response object
        """
        params = {}
        return self.Call("GetSystemTime", id, params)

    def GetConfiguration(self, id, name:str, verbsity:str):
        """
        ZEDO RPC call: Obtain board unit (AE sensor) configurations

        :param name: Union[str, List[str]] - Name of sensor (=board unit) or array of names for sensors for which a configuration is to be returned
        :param verbosity: str - Required verbosity of output; examples: "min", "gain|pulser", .. default is "all"
        :return: Promise<(Object | Array<Object>)> '.then' returns configuration object or array of objects (depending on input type)
        """ 
        params = {
            "name": name,
            "verbsity": verbsity,
        }
        return self.Call("GetConfiguration", id, params)

    def Configure(self, id, config:object, verbosity:str):
        """
        ZEDO RPC call: Configure one or more sensors, return the actual configuration objects

        :param config: Union[Dict, List[Dict]] - One object or array of objects to configure ('name' must be a member)
        :param verbosity: str - Required verbosity of output; examples: "min", "gain|pulser", .. default is "all"
        :return: Promise .then returns confirmed configuration object or array of configuration objects (depending on input type)
        """
        params = {
            "config": config,
            "verbosity": verbosity,
        }
        return self.Call("Configure", id, params)

    def ClearLiveData(self, id):
        """
        ZEDO RPC call: Clear live data and reset relative measurement time to 0

        :return: Promise '.then' returns the response object (check .status to be zero)
        """
        params = { }
        return self.Call("ClearLiveData", id, params)

    def StartRecording(self, id, measurement_name:str = "pokus", record_history_secs:int = 1000):
        """
        ZEDO RPC call: Start data recording

        :param measurement_name: str - optional, name of the recording. ZDaemon will decide its own name if not specified.
        :param record_history_secs: int - optional, number of seconds to record from data buffers. (optional, default 0)
        :return: Promise '.then' returns the response object (check .status to be zero)
        """
        params = {
            "measurement_name": measurement_name,
            "record_history_secs": record_history_secs,
        }
        return self.Call("StartRecording", id, params)

    def PauseRecording(self, id):
        """
        ZEDO RPC call: Pause data recording
        :return: Promise '.then' returns the response object (check .status to be zero)
        """ 
        params = {}
        return self.Call("PauseRecording", id, params)

    def StopRecording(self, id):
        """
        ZEDO RPC call: Stop data recording

        :return: Promise '.then' returns the response object (check .status to be zero)
        """
        params = { }
        return self.Call("StopRecording", id, params)

    def GetRecordingState(self, id):
        """
        ZEDO RPC call: Determine recording status

        :return: Promise '.then' returns the response object (check .status to be zero)
        """
        params = { }
        return self.Call("GetRecordingState", id, params)

    def GetAppInfo(self, id):
        """
        ZEDO RPC call: Get ZDaemon application information

        :return: Promise<Object> '.then' returns the information object
        """ 
        params = { }
        return self.Call("GetAppInfo", id, params)

    def GetActivePulsers(self, id, passives_too:bool):
        """
        Get array of board units with activated pulser

        :param passives_too: Boolean Also include items configured for passive mode
        :return: Promise '.then' returns the array of objects with an active pulser
        """
        params = {
            "passives_too": passives_too,
        }
        return self.Call("GetActivePulsers", id, params)

    def AllPulsersOff(self, id, passives_too:bool):
        """
        Make sure all pulsers are off

        :param passives_too: Boolean Also include items configured for passive mode
        :return: Promise '.then' returns the array of objects with an active pulser
        """
        params = {
            "passives_too": passives_too,
        }
        return self.Call("AllPulsersOff", id, params)

    def pulser_configs_same(self, id, p1:object, p2:object):
        """
        Compare if two pulser configurations are the same, ignore irrelevant parameters

        :param p1: Object Pulser configuration object 1
        :param p2: Object Pulser configuration object 2
        :return: Boolean Returns true when configurations are the same
        """
        params = {
            "p1": p1,
            "p2": p2,
        }
        return self.Call("pulser_configs_same", id, params)

    def SetPulser(self, id, name:str, pulser:object, retries:int = 3, retry_delay_ms:int = 333):
        """
        Set given board unit to specified pulser mode. This function may attempt to retry if pulser activation fails.

        :param name: String Board unit name which is to be configured.
        :param pulser: Object Pulser configuration object
        :param retries: Number Number of retries (optional, default 3)
        :param retry_delay_ms: Number Hold time after retrying (optional, default 333)
        :return: Promise '.then' returns the array of objects with configured pulser
        """
        params = {
            "name": name,
            "pulser": pulser,
            "retries": retries,
            "retry_delay_ms": retry_delay_ms,
        }
        return self.Call("SetPulser", id, params)

    def EnableContinuousRecording(self, id, name:str, enable:bool):
        """
        Enable or disable continuous recording on selected boards (by names)

        :param name: String | Array<String> Board unit name or array of names which are to be configured.
        :param enable: Number 0 to disable continuous recording, 1 to enable it, 2 to enable it when recording
        :return: Promise '.then' returns the array of objects with configured continuous recording
        """
        params = {
            "name": name,
            "enable": enable,
        }
        return self.Call("EnableContinuousRecording", id, params)

    def OpenFileReaderByPath(self, id, path:str):
        """
        ZEDO RPC call: Open new or locate existing FileReader object with specific set of source paths

        :param path: String | Array<String> Source data directory or directories to open.
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """
        params = {
            "path": path,
        }
        return self.Call("OpenFileReaderByPath", id, params)

    def OpenFileReaderByName(self, id, name:str = "pokus"):
        """
        ZEDO RPC call: Lookup an existing FileReader object of a given name

        :param name: String FileReader object name. If name is empty, the default (first) existing FileReader will be located. (optional, default "")
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """
        params = {
            "name": name,
        }
        return self.Call("OpenFileReaderByName", id, params)

    def SetFileReaderPath(self, id, reader_id:int, path:str, update_name:bool):
        """
        ZEDO RPC call: Re-configure FileReader and assign it a new source path

        :param reader_id: Number File reader ID received from OpenFileReaderXXX methods
        :param path: String | Array<String> Source data directory or directories to open.
        :param update_name: Boolean Let the file reader to change its name based on the source data path. (optional, default false)
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """
        params = {
            "reader_id": reader_id,
            "path": path,
            "update_name": update_name,
        }
        return self.Call("SetFileReaderPath", id, params)

    def GetFileReaderInfo(self, id, reader_id:int = 100084):
        """
        ZEDO RPC call: Get File Reader information

        :param reader_id: Number File reader ID received from OpenFileReaderXXX methods
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """
        params = {
            "reader_id": reader_id,
        }
        params = {"reader_id": reader_id}
        return self.Call("GetFileReaderInfo", id, params)

    def GetFileReaderData(self, id, reader_id:int = 100084):
        """
        ZEDO RPC call: Get File Reader information, list of boards / units and items

        :param reader_id: Number File reader ID received from OpenFileReaderXXX methods
        :return: Promise<Array> '.then' returns the response object
        """
        params = {
            "reader_id": reader_id,
        }
        return self.Call("GetFileReaderData", id, params)

    def ExportFileReaderData(self, id, reader_id:int, outdir:str, subdir:str, export_cfg:object, make_unique_dir:bool):
        """
        ZEDO RPC call: Export file reader data

        :param reader_id: Number File reader ID received from OpenFileReaderXXX methods
        :param outdir: Output directory
        :param subdir: Subdirectory
        :param export_cfg: Object Export configuration. Use ZDaemon GUI to generate a template.
        :param make_unique_dir: Boolean (optional, default true)
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """
        params = {
            "reader_id": reader_id,
            "outdir": outdir,
            "subdir": subdir,
            "export_cfg": export_cfg,
            "make_unique_dir": make_unique_dir,
        }
        return self.Call("ExportFileReaderData", id, params)

    def ExportItems(self, id, items:str, outdir:str, subdir:str, export_cfg:object, make_unique_dir:bool):
        """
        ZEDO RPC call: Export multiple file readers or other item's data

        :param items: Name or array of names of items to be exported ("_id:NNN" is also accepted as a name)
        :param outdir: Output directory
        :param subdir: Subdirectory (optional, default "graphs")
        :param export_cfg: Object Export configuration. See ExportFileReaderData for more information. Additional allow and deny items are possible when localization group is exported. Examples: "l_locevn", "locfilt"
        :param make_unique_dir: Boolean If 'subdir' is specified, it will be modified to be unique within outdir (optional, default true)
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """
        params = {
            "items": items,
            "outdir": outdir,
            "subdir": subdir,
            "export_cfg": export_cfg,
            "make_unique_dir": make_unique_dir,
        }
        return self.Call("ExportItems", id, params)

    def CaptureGraphPictures(self, id, subdir:str, export_cfg:object, make_unique_dir:bool, make_unique_files:bool):
        """
        Capture graph pictures currently open in ZDaemon into a specific folder.

        :param outdir: Output directory
        :param subdir: Subdirectory (optional, default "graphs")
        :param make_unique_dir: Boolean If 'subdir' is specified, it will be modified to be unique within outdir (optional, default true)
        :param make_unique_files: Boolean Make the files unique if output directory and files already exist (optional, default true)
        :return: Promise<Object> '.then' returns the response object
        """
        params = {
            "subdir": subdir,
            "export_cfg": export_cfg,
            "make_unique_dir": make_unique_dir,
            "make_unique_files": make_unique_files,
        }
        return self.Call("CaptureGraphPictures", id, params)

    def WaitFileReaderScanned(self, id, reader_id:int):
        """
        ZEDO RPC call: Wait until File Reader finishes file scanning

        :param reader_id: Number File reader ID received from OpenFileReader
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """ 
        params = {
            "reader_id": reader_id,
        }
        return self.Call("WaitFileReaderScanned", id, params)

    def WaitItemsIdle(self, id, items:str):
        """
        ZEDO RPC call: Wait until all specified items and their child items are idle.

        :param items: Name or array of names of items to be exported ("_id:NNN" is also accepted as a name)
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """
        params = {
            "items": items,
        }
        return self.Call("WaitItemsIdle", id, params)

    def GetExportJobStatus(self, id, job_id:int):
        """
        ZEDO RPC call: Get status of File Reader Export Job

        :param job_id: Int - Export Job ID received from ExportFileReaderData
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """
        params = {
            "job_id": job_id,
        }
        return self.Call("GetExportJobStatus", id, params)

    def AbortExportJob(self, id, job_id:int):
        """
        ZEDO RPC call: Abort File Reader Export Job

        :param job_id: Export Job ID received from ExportFileReaderData
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """
        params = {
            "job_id": job_id,
        }
        return self.Call("AbortExportJob", id, params)

    def WaitBackroundJobFinished(self, id, job_id:int, timeout_seconds:int = 10):
        """
        ZEDO RPC call: Wait until File Reader Export Job finishes with timeout

        :param job_id: Export Job ID received from ExportFileReaderData
        :param timeout_seconds: Total operation timeout in seconds. Use 0 to disable timeout.
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """
        params = {
            "job_id": job_id,
            "timeout_seconds": timeout_seconds,
        }
        return self.Call("WaitBackroundJobFinished", id, params)

    def ExportJobProgressMonitor(self, id, job_id:int, period_sec:int, timeout_sec:int, proggress_callback):
        """
        ZEDO RPC call: Start timer to call GetExportJobStatus periodically to monitor the export job

        :param job_id: Export Job ID received from ExportFileReaderData
        :param period_sec: Status checking period in seconds
        :param timeout_sec: Total operation timeout in seconds. Use 0 to disable timeout.
        :param progress_callback: User function called each period to report GetExportJobStatus. Callback may return true to abort waiting.
        :return: Promise<Object> Resolved when export is finished, when callback aborts it or when timeout occurs. Rejected in case of error.
        """
        params = {
            "job_id": job_id,
            "period_sec": period_sec,
            "timeout_sec": timeout_sec,
            "proggress_callback": proggress_callback,
        }
        return self.Call("ExportJobProgressMonitor", id, params)

    def GetItemInfo(self, id, name:str, verbosity:str = "max"):
        """
        ZEDO RPC call: Determine if item exists and get its description

        :param name: Name of item to be retrieve ("_id:NNN" is also accepted as a name)
        :param verbosity: Required verbosity of output; examples: "min", "med", "max", "all" (optional, default "max")
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """
        params = {
            "name": name,
            "verbosity": verbosity,
        }
        return self.Call("GetItemInfo", id, params)

    def GetSubItems(self, id, name:str):
        """
        ZEDO RPC call: Get sub-items of a specified item

        :param name: Name of item to be retrieve ("_id:NNN" is also accepted as a name)
        :return: Promise<Object> '.then' returns the response object (check .status to be zero)
        """
        params = {
            "name": name,
        }
        return self.Call("GetSubItems", id, params)

# Příklad použití třídy
if __name__ == "__main__":
    sensor = SensorController("192.168.0.196", 40999)
    sensor.Connect()
    # response_string = sensor.GetSystemTime("001")
    # response_string = sensor.GetSensors("001")
    # response_string = sensor.GetConfiguration("001") {"jsonrpc":"2.0","id":"001","error":{"code":3,"message":"Unknown method: GetConfiguration"}}
    #response_string = sensor.StartRecording("001")
    # response_string = sensor.StopRecording("001")
    # response_string = sensor.OpenFileReaderByName("001")
    # response_string = sensor.GetFileReaderInfo("001")
    # response_string = sensor.GetFileReaderData("001")

    # Vypsání odpovědi
    # print("Response from server:", response_string)
