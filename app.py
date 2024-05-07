################################################
## Project: ASS/NSS API 
## Author: David Michalica, Team 1
## Date: 2024
## 
## Documentation: https://medium.com/@asvinjangid.kumar/creating-your-own-api-in-python-a-beginners-guide-59f4dd18d301
#################################################

import os
from flask import Flask, jsonify, abort 
from config import Config

from BussinessLayer.MultiSpectral_Camera_Controller import Multispectral_Camera_Controller
from BussinessLayer.RGB_Camera_Controller import RGB_Camera_Controller
from BussinessLayer.SensorController import SensorController
 
from data.RGB_camera import RGB_Camera_Start

# instance of flask application
app = Flask(__name__)
app.config.from_object(Config)
#from .routes import api
#app.register_blueprint(api)


def GetSensorController(ip, port):
    return SensorController(ip, port)

def GetMultispecCameraController():
    return Multispectral_Camera_Controller()

def GetRGB_Camera_Controller():
    return RGB_Camera_Controller()

# home route that returns below text when root url is accessed
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# RGB camera endpoints
@app.route('/sensor/rgb/start', methods=['GET'])
def CameraRgbStart(config:RGB_Camera_Start):
    rGB_Camera_Controller = GetRGB_Camera_Controller()
    rGB_Camera_Controller.Connect()
    data = rGB_Camera_Controller.capture_image(path = config.path, name = config.name, count = config.name, quality = config.quality, image_format=config.image_format)
    return jsonify(data)

@app.route('/sensor/rgb/config', methods=['GET'])
def CameraRgbConfig(config:RGB_Camera_Start):
    rGB_Camera_Controller = GetRGB_Camera_Controller()
    return jsonify(
        {
            "data_type:": rGB_Camera_Controller.save_functions.keys,
            "width": rGB_Camera_Controller.camera.Width.Value,
            "height": rGB_Camera_Controller.camera.Height.Value,
        }
    )



# Acustic Sensor endpoints
@app.route('/sensor/acustic/start', methods=['GET'])
def SensorAcusticStart(ip:str = "192.168.0.196", port:int = 40999):
    sensorController = GetSensorController(ip, port)
    return jsonify(sensorController.StartRecording("001"))

@app.route('/sensor/acustic/stop', methods=['GET'])
def SensorAcusticStop(ip:str = "192.168.0.196", port:int = 40999):
    sensorController = GetSensorController(ip, port)
    return jsonify(sensorController.StopRecording("001"))

@app.route('/sensor/acustic/pause', methods=['POST'])
def SensorAcusticPause(ip:str = "192.168.0.196", port:int = 40999):
    sensorController = GetSensorController(ip, port)
    return jsonify(sensorController.PauseRecording("001"))

@app.route('/sensor/acustic/state', methods=['POST'])
def SensorAcusticState(ip:str = "192.168.0.196", port:int = 40999):
    sensorController = GetSensorController(ip, port)
    return jsonify(sensorController.GetRecordingState("001"))

@app.route('/sensor/acustic/', methods=['GET'])
def SensorAcustic(ip:str = "192.168.0.196", port:int = 40999):
    sensorController = GetSensorController(ip, port)
    return jsonify({
        "sensors": sensorController.GetSensors,
        "time": sensorController.GetSystemTime,
    })

@app.route('/sensor/acustic/config', methods=['GET'])
def SensorAcusticConfig(name:str, verbosity:str, ip:str = "192.168.0.196", port:int = 40999):
    sensorController = GetSensorController(ip, port)
    return jsonify({
        "config": sensorController.GetConfiguration("001", name=name, verbsity=verbosity),
    })

@app.route('/sensor/acustic/config', methods=['POST'])
def SensorAcusticConfigSet(config:object, verbosity:str, ip:str = "192.168.0.196", port:int = 40999):
    sensorController = GetSensorController(ip, port)
    return jsonify({
        "config": sensorController.Configure("001", config=config, verbsity=verbosity),
    })
 
if __name__ == '__main__':  
   port = int(os.environ.get('PORT', 5000))
   app.run(debug = True, host='0.0.0.0', port=port)
   # "192.168.0.196", 40999
