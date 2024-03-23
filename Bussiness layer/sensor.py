################################################
## Project: ASS/NSS API 
## Author: David Michalica, Team 1
## Date: 2024
## 
## Documentation: https://bitbucket.org/dakel/node-zedo-rpc/src/master/API.md
## alternativni knihovny pro py: pyro4, xmlrpc.server, jsonrpcserver, zerorpc
#################################################

from jsonrpcserver import method, async_dispatch as dispatch

class SensorController:
    def __init__(self):
        # inicializace senzoru, například připojení, nastavení, atd.

    @method
    async def start_recording(self):
        # implementace operace pro start záznamu
        return "Recording started."

    @method
    async def pause_recording(self):
        # implementace operace pro pozastavení záznamu
        return "Recording paused."

    @method
    async def stop_recording(self):
        # implementace operace pro zastavení záznamu
        return "Recording stopped."

    @method
    async def get_file_reader(self):
        # implementace operace pro získání čtečky souborů
        return "File reader obtained."

# Příklad použití třídy
if __name__ == "__main__":
    sensor_controller = SensorController()
    requests = [
        '{"jsonrpc": "2.0", "method": "start_recording", "params": {}, "id": 1}',
        '{"jsonrpc": "2.0", "method": "pause_recording", "params": {}, "id": 2}',
        '{"jsonrpc": "2.0", "method": "stop_recording", "params": {}, "id": 3}',
        '{"jsonrpc": "2.0", "method": "get_file_reader", "params": {}, "id": 4}'
    ]
    for request in requests:
        response = await dispatch(request, sensor_controller)
        print(response)
