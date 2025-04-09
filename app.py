################################################
## Project: ASS/NSS API
## Author: David Michalica, Team 1
## Date: 2024
##
## Documentation: https://medium.com/@asvinjangid.kumar/creating-your-own-api-in-python-a-beginners-guide-59f4dd18d301
#################################################

import logging
import os

from flask import Flask, Response, jsonify, request
from flask_cors import CORS

from BussinessLayer.RGB_Camera_Controller import RGB_Camera_Controller
from BussinessLayer.SensorController import SensorController
from config import Config

# Set up logging
logging.basicConfig(
    level=Config.get_log_level(),
    format=Config.LOG_FORMAT,
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")],
)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # Enable CORS for all routes

# Create data directory if it doesn't exist
os.makedirs(Config.DEFAULT_STORAGE_PATH, exist_ok=True)


def get_sensor_controller(ip: str, port: int) -> SensorController:
    """
    Creates and returns a SensorController instance.

    Args:
        ip (str): The IP address of the sensor
        port (int): The port to connect to

    Returns:
        SensorController: A configured SensorController instance
    """
    try:
        controller = SensorController(ip, port)
        controller.Connect()
        return controller
    except Exception as e:
        logger.error(f"Failed to create SensorController: {str(e)}")
        raise


def get_rgb_camera_controller() -> RGB_Camera_Controller:
    """
    Creates and returns an RGB_Camera_Controller instance.

    Returns:
        RGB_Camera_Controller: A configured RGB_Camera_Controller instance
    """
    try:
        return RGB_Camera_Controller(
            camera_width=Config.DEFAULT_RGB_CAMERA_WIDTH,
            camera_height=Config.DEFAULT_RGB_CAMERA_HEIGHT,
            camera_format=Config.DEFAULT_RGB_CAMERA_FORMAT,
        )
    except Exception as e:
        logger.error(f"Failed to create RGB_Camera_Controller: {str(e)}")
        raise


@app.route("/")
def hello_world() -> str:
    """
    Root endpoint for the API.

    Returns:
        str: A greeting message
    """
    return "<p>Hello, World! Welcome to the ASS/NSS API</p>"


@app.route("/health")
def health_check() -> Response:
    """
    Health check endpoint for the API.

    Returns:
        Response: JSON response with health status
    """
    return jsonify(
        {"status": "ok", "environment": os.environ.get("FLASK_ENV", "development")}
    )


# RGB camera endpoints
@app.route("/sensor/rgb/start", methods=["POST"])
def camera_rgb_start() -> Response:
    """
    Endpoint to start RGB camera and capture image.

    Returns:
        Response: JSON response with image capture results
    """
    try:
        config = request.json
        if not config:
            return jsonify({"error": "No configuration provided"}), 400

        required_fields = ["path", "name", "quality", "image_format"]
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

        rgb_camera_controller = get_rgb_camera_controller()
        rgb_camera_controller.Connect()

        data = rgb_camera_controller.capture_image(
            path=config["path"],
            name=config["name"],
            count=config.get("count", 1),
            quality=config["quality"],
            image_format=config["image_format"],
        )

        return jsonify({"success": True, "data": data})
    except Exception as e:
        logger.error(f"Error in camera_rgb_start: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/sensor/rgb/config", methods=["GET"])
def camera_rgb_config() -> Response:
    """
    Endpoint to get RGB camera configuration.

    Returns:
        Response: JSON response with camera configuration
    """
    try:
        rgb_camera_controller = get_rgb_camera_controller()
        rgb_camera_controller.Connect()

        config_data = {
            "data_types": list(rgb_camera_controller.save_functions.keys()),
            "width": rgb_camera_controller.camera.Width.Value,
            "height": rgb_camera_controller.camera.Height.Value,
            "default_config": {
                "width": Config.DEFAULT_RGB_CAMERA_WIDTH,
                "height": Config.DEFAULT_RGB_CAMERA_HEIGHT,
                "format": Config.DEFAULT_RGB_CAMERA_FORMAT,
            },
        }

        # Properly release the camera
        rgb_camera_controller.release_camera()

        return jsonify(config_data)
    except Exception as e:
        logger.error(f"Error in camera_rgb_config: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Acoustic Sensor endpoints
@app.route("/sensor/acoustic/start", methods=["POST"])
def sensor_acoustic_start() -> Response:
    """
    Endpoint to start acoustic sensor recording.

    Returns:
        Response: JSON response with recording start results
    """
    try:
        data = request.json or request.form
        if not data or "ip" not in data or "port" not in data:
            # Use default configuration if not provided
            ip = Config.DEFAULT_SENSOR_IP
            port = Config.DEFAULT_SENSOR_PORT
            logger.info(f"Using default sensor configuration: {ip}:{port}")
        else:
            ip = data["ip"]
            port = int(data["port"])

        sensor_controller = get_sensor_controller(ip, port)
        measurement_name = data.get("measurement_name", "001")

        result = sensor_controller.StartRecording(measurement_name)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in sensor_acoustic_start: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/sensor/acoustic/stop", methods=["POST"])
def sensor_acoustic_stop() -> Response:
    """
    Endpoint to stop acoustic sensor recording.

    Returns:
        Response: JSON response with recording stop results
    """
    try:
        data = request.json or request.form
        if not data or "ip" not in data or "port" not in data:
            # Use default configuration if not provided
            ip = Config.DEFAULT_SENSOR_IP
            port = Config.DEFAULT_SENSOR_PORT
            logger.info(f"Using default sensor configuration: {ip}:{port}")
        else:
            ip = data["ip"]
            port = int(data["port"])

        sensor_controller = get_sensor_controller(ip, port)
        measurement_name = data.get("measurement_name", "001")

        result = sensor_controller.StopRecording(measurement_name)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in sensor_acoustic_stop: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/sensor/acoustic/pause", methods=["POST"])
def sensor_acoustic_pause() -> Response:
    """
    Endpoint to pause acoustic sensor recording.

    Returns:
        Response: JSON response with recording pause results
    """
    try:
        data = request.json or request.form
        if not data or "ip" not in data or "port" not in data:
            # Use default configuration if not provided
            ip = Config.DEFAULT_SENSOR_IP
            port = Config.DEFAULT_SENSOR_PORT
            logger.info(f"Using default sensor configuration: {ip}:{port}")
        else:
            ip = data["ip"]
            port = int(data["port"])

        sensor_controller = get_sensor_controller(ip, port)
        measurement_name = data.get("measurement_name", "001")

        result = sensor_controller.PauseRecording(measurement_name)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in sensor_acoustic_pause: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/sensor/acoustic/state", methods=["GET"])
def sensor_acoustic_state() -> Response:
    """
    Endpoint to get acoustic sensor recording state.

    Returns:
        Response: JSON response with recording state
    """
    try:
        data = request.args or request.form
        if not data or "ip" not in data or "port" not in data:
            # Use default configuration if not provided
            ip = Config.DEFAULT_SENSOR_IP
            port = Config.DEFAULT_SENSOR_PORT
            logger.info(f"Using default sensor configuration: {ip}:{port}")
        else:
            ip = data["ip"]
            port = int(data["port"])

        sensor_controller = get_sensor_controller(ip, port)
        measurement_name = data.get("measurement_name", "001")

        result = sensor_controller.GetRecordingState(measurement_name)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in sensor_acoustic_state: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/sensor/acoustic/info", methods=["GET"])
def sensor_acoustic_info() -> Response:
    """
    Endpoint to get acoustic sensor information.

    Returns:
        Response: JSON response with sensor information
    """
    try:
        data = request.args or request.form
        if not data or "ip" not in data or "port" not in data:
            # Use default configuration if not provided
            ip = Config.DEFAULT_SENSOR_IP
            port = Config.DEFAULT_SENSOR_PORT
            logger.info(f"Using default sensor configuration: {ip}:{port}")
        else:
            ip = data["ip"]
            port = int(data["port"])

        sensor_controller = get_sensor_controller(ip, port)

        result = {
            "sensors": sensor_controller.GetSensors("info"),
            "time": sensor_controller.GetSystemTime("time"),
        }
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in sensor_acoustic_info: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/sensor/acoustic/config", methods=["GET"])
def sensor_config_get() -> Response:
    """
    Endpoint to get acoustic sensor configuration.

    Returns:
        Response: JSON response with sensor configuration
    """
    try:
        data = request.args or request.form
        if not data or "ip" not in data or "port" not in data:
            # Use default configuration if not provided
            ip = Config.DEFAULT_SENSOR_IP
            port = Config.DEFAULT_SENSOR_PORT
            logger.info(f"Using default sensor configuration: {ip}:{port}")
        else:
            ip = data["ip"]
            port = int(data["port"])

        sensor_controller = get_sensor_controller(ip, port)
        measurement_name = data.get("measurement_name", "001")
        verbosity = data.get("verbosity", "all")

        result = {
            "config": sensor_controller.GetConfiguration(measurement_name, verbosity)
        }
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in sensor_config_get: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/sensor/acoustic/config", methods=["POST"])
def sensor_config_set() -> Response:
    """
    Endpoint to set acoustic sensor configuration.

    Returns:
        Response: JSON response with configuration set results
    """
    try:
        data = request.json
        if not data or "ip" not in data or "port" not in data or "config" not in data:
            return jsonify({"error": "Missing required parameters"}), 400

        sensor_controller = get_sensor_controller(data["ip"], int(data["port"]))
        measurement_name = data.get("measurement_name", "001")
        verbosity = data.get("verbosity", "all")

        result = {
            "config": sensor_controller.Configure(
                measurement_name, data["config"], verbosity
            )
        }
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in sensor_config_set: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/config")
def get_app_config() -> Response:
    """
    Endpoint to get the current application configuration (excluding sensitive info).

    Returns:
        Response: JSON response with application configuration
    """
    # Filter out private attributes and functions
    config_dict = {
        k: v
        for k, v in Config.to_dict().items()
        if not k.startswith("_") and not callable(v)
    }

    # Remove any sensitive information if needed
    # sensitive_keys = ["API_KEY", "SECRET_KEY"]
    # for key in sensitive_keys:
    #     if key in config_dict:
    #         config_dict[key] = "***REDACTED***"

    return jsonify({"config": config_dict})


if __name__ == "__main__":
    # Get port and host from config
    port = Config.PORT
    host = Config.HOST

    logger.info(f"Starting ASS/NSS API on {host}:{port}")
    logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    logger.info(f"Debug mode: {'enabled' if Config.DEBUG else 'disabled'}")

    app.run(debug=Config.DEBUG, host=host, port=port)
