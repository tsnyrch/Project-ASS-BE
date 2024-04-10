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


    def Generate_rec_folder_name(self, id, prefix, use_date, use_m, use_sec, name_delimeter, time_delimeter, now):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        params = {
            "prefix": prefix,
            "use_date": use_date,
            "use_m": use_m,
            "use_sec": use_sec,
            "name_delimeter": name_delimeter
        }
        return self.Call(self.methods["GRFN"], id, params)

    def Compare_versions(self, id, ver_a, ver_b):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("Compare_versions", id)

    def Assert_min_version(self, id, min_version, assert_time):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("Assert_min_version", id)

    def Copy_json(self, id, obj):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("Copy_json", id)

    def Print_json(self, id, obj):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("Print_json", id)

    def Is_json_object(self, id, obj):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("Is_json_object", id)

    def Merge_json(self, id, dest, src, overwrite_values, overwrite_objects):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("Merge_json", id)

    def Is_zdat_directory(self, id, path):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("Is_zdat_directory", id)

    def GetSensors(self, id, verbosity):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("GetSensors", id)

    def GetSystemStatus(self, id):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("GetSystemStatus", id)

    def GetSystemTime(self, id):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("GetSystemTime", id)

    def GetConfiguration(self, id, name, verbsity):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("GetConfiguration", id)

    def Configure(self, id, config, verbosity):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("Configure", id)

    def ClearLiveData(self, id):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("ClearLiveData", id)

    def StartRecording(self, id, measurement_name = "pokus", record_history_secs = 0):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        params = {"measurement_name": measurement_name, "record_history_secs": record_history_secs}
        return self.Call("StartRecording", id)

    def PauseRecording(self, id):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("PauseRecording", id)

    def StopRecording(self, id):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("StopRecording", id)

    def GetRecordingState(self, id):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("GetRecordingState", id)

    def GetAppInfo(self, id):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("GetAppInfo", id)

    def GetActivePulsers(self, id, passives_too):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("GetActivePulsers", id)

    def AllPulsersOff(self, id, passives_too):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("AllPulsersOff", id)

    def pulser_configs_same(self, id, p1, p2):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("pulser_configs_same", id)

    def SetPulser(self, id, name, pulser, retries, retry_delay_ms):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("SetPulser", id)

    def EnableContinuousRecording(self, id, name, enable):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("EnableContinuousRecording", id)

    def OpenFileReaderByPath(self, id, path):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("OpenFileReaderByPath", id)

    def OpenFileReaderByName(self, id, name = "pokus"):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        params = {"name": name}
        return self.Call("OpenFileReaderByName", id, params)

    def SetFileReaderPath(self, id, reader_id, path, update_name):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("SetFileReaderPath", id)

    def GetFileReaderInfo(self, id, reader_id = 100084):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        params = {"reader_id": reader_id}
        return self.Call("GetFileReaderInfo", id)

    def GetFileReaderData(self, id, reader_id = 100084):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        params = {"reader_id": reader_id}
        return self.Call("GetFileReaderData", id, params)

    def ExportFileReaderData(self, id, reader_id, outdir, subdir, export_cfg, make_unique_dir):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("ExportFileReaderData", id)

    def ExportItems(self, id, items, outdir, subdir, export_cfg, make_unique_dir):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("ExportItems", id)

    def CaptureGraphPictures(self, id, subdir, export_cfg, make_unique_dir, make_unique_files):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("CaptureGraphPictures", id)

    def WaitFileReaderScanned(self, id, reader_id):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("WaitFileReaderScanned", id)

    def WaitItemsIdle(self, id, items):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("WaitItemsIdle", id)

    def GetExportJobStatus(self, id, job_id):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("GetExportJobStatus", id)

    def AbortExportJob(self, id, job_id):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("AbortExportJob", id)

    def WaitBackroundJobFinished(self, id, job_id, timeout_seconds):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("WaitBackroundJobFinished", id)

    def ExportJobProgressMonitor(self, id, job_id, period_sec, timeout_sec, proggress_callback):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("ExportJobProgressMonitor", id)

    def GetItemInfo(self, id, name, verbosity):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("GetItemInfo", id)

    def GetSubItems(self, id, name):
        """
        Generate_rec_folder_name - .

        :param id: describe about parameter p1
        :param : describe about parameter p2
        :param : describe about parameter p3
        :return: describe what it returns
        """ 
        return self.Call("GetSubItems", id)

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
