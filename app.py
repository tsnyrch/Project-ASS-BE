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
#import BussinessLayer.SensoreService
#from BussinessLayer.MultiSpectral_Camera_Controller import Multispectral_Camera_Controller
from BussinessLayer.RGB_Camera_Controller import RGB_Camera_Controller
from BussinessLayer.SensorController import SensorController
 
from data.RGB_camera import RGB_Camera_Start

# instance of flask application
app = Flask(__name__)
app.config.from_object(Config)
#from .routes import api
#app.register_blueprint(api)

# definition of confrollers
sensorController = SensorController("192.168.0.196", 40999)
#multispectral_Camera_Controller = Multispectral_Camera_Controller()
rGB_Camera_Controller = RGB_Camera_Controller()

# home route that returns below text when root url is accessed
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# RGB camera endpoints
@app.route('/sensor/rgb/start', methods=['GET'])
def SensorStart(config:RGB_Camera_Start):
    data = rGB_Camera_Controller.capture_image(path = config.path, name = config.name, count = config.name, quality = config.quality, image_format=config.image_format)
    return jsonify(data)

@app.route('/sensor/rgb/config', methods=['GET'])
def SensorStart(config:RGB_Camera_Start):
    return jsonify(
        {
            "data_type:": rGB_Camera_Controller.save_functions.keys,
            "width": rGB_Camera_Controller.camera.Width.Value,
            "height": rGB_Camera_Controller.camera.Height.Value,
        }
    )

# Acustic Sensor endpoints
@app.route('/sensor/acustic/config', methods=['GET'])
def SensoreStop():
    return jsonify(message='Hello, World!')

@app.route('/sensor/acustic/start', methods=['GET'])
def SensoreStop():
    ##
    try:
        result = {
            "time": sensorController.GetSystemTime,
            "sensors": sensorController.GetSensors("001"),
            "config": sensorController.GetConfiguration("001"),
            "recording": sensorController.StartRecording("001"),
            "reader": sensorController.OpenFileReaderByName("001"),
            "reader_info": sensorController.GetFileReaderInfo("001"),
            "reader_data": sensorController.GetFileReaderData("001")
        }
        return jsonify(result)
    except:
        abort(500)

@app.route('/sensor/acustic/data', methods=['POST'])
def SensoreStop():
    return jsonify(message='Hello, World!')
 
if __name__ == '__main__':  
   port = int(os.environ.get('PORT', 5000))
   app.run(debug = True, host='0.0.0.0', port=port)
