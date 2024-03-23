################################################
## Project: ASS/NSS API 
## Author: David Michalica, Team 1
## Date: 2024
## 
## Documentation: https://medium.com/@asvinjangid.kumar/creating-your-own-api-in-python-a-beginners-guide-59f4dd18d301
#################################################

from flask import Blueprint, jsonify
import subprocess

api = Blueprint('api', __name__)

@api.route('/hello', methods=['GET'])
def hello():
    return jsonify(message='Hello, World!')

@app.route('/date', methods=['GET'])
def get_date():
    result = subprocess.check_output(['date']).decode('utf-8')
    return jsonify({'date': result.strip()})

@app.route('/cal', methods=['GET'])
def get_cal():
    result = subprocess.check_output(['cal']).decode('utf-8')
    return jsonify({'calendar': result.strip()})

@app.route('/docker', methods=['GET'])
def get_docker():
    result = subprocess.check_output(['docker', 'ps']).decode('utf-8')
    return jsonify({'docker': result.strip()})

@app.route('/cls', methods=['GET'])
def get_cls():
    result = subprocess.check_output(['cls']).decode('utf-8')
    return jsonify({'cls': result.strip()})

if __name__ == '__main__':
    app.run()