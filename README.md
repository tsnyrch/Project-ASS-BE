# ASS/NSS API Project

## Overview

The ASS/NSS API is a Python Flask application that provides an interface for controlling RGB cameras and acoustic sensors. It's designed for data acquisition and sensor management in scientific and industrial applications.

## Features

- RGB Camera control using Pypylon for Basler cameras
- Acoustic sensor interfacing
- RESTful API endpoints for sensor control
- Docker support for easy deployment
- Environment-based configuration

## Project Structure

```
Project-ASS-BE/
├── app.py                   # Main application file
├── config.py                # Configuration settings
├── .env                     # Environment variables
├── compose.yaml             # Docker Compose configuration
├── Dockerfile               # Docker configuration
├── BussinessLayer/          # Business logic
│   ├── RGB_Camera_Controller.py       # RGB camera control
│   ├── MultiSpectral_Camera_Controller.py # Multispectral camera control
│   └── SensorController.py  # Acoustic sensor control
├── data/                    # Data models
│   └── RGB_camera.py        # RGB camera data models
├── UnitTests/               # Unit tests
│   └── GeneralTest.py       # General API tests
└── requirements.txt         # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+
- Pypylon (for Basler cameras)
- Flask
- Docker (optional)

### Installation

#### Local Installation

1. Clone the repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables (copy from .env.example):
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```
4. Run the application:
   ```bash
   python app.py
   ```

#### Docker Installation

1. Configure environment variables:

   ```bash
   # Edit .env file with your settings
   ```

2. Build and start the container:
   ```bash
   docker compose up
   ```
3. To run in detached mode:
   ```bash
   docker compose up -d
   ```

## Configuration

The application can be configured via environment variables in the `.env` file:

- `FLASK_ENV` - Environment mode (development, testing, production)
- `PORT` - Port for the Flask application (default: 5005)
- `HOST` - Host address for the Flask application (default: 0.0.0.0)
- `DEFAULT_RGB_CAMERA_WIDTH` - Default RGB camera width (default: 1920)
- `DEFAULT_RGB_CAMERA_HEIGHT` - Default RGB camera height (default: 1080)
- `DEFAULT_RGB_CAMERA_FORMAT` - Default RGB camera format (default: RGB8)
- `CAMERA_DEVICE` - Camera device path (default: /dev/null)
- `DEFAULT_SENSOR_IP` - Default IP for acoustic sensors (default: 192.168.0.196)
- `DEFAULT_SENSOR_PORT` - Default port for acoustic sensors (default: 40999)
- `DEFAULT_STORAGE_PATH` - Default path for storing captured data (default: ./storage/)
- `LOG_LEVEL` - Logging level (default: INFO)

## API Endpoints

### RGB Camera Endpoints

- `GET /sensor/rgb/config` - Get RGB camera configuration
- `POST /sensor/rgb/start` - Start RGB camera and capture images

### Acoustic Sensor Endpoints

- `POST /sensor/acoustic/start` - Start acoustic sensor recording
- `POST /sensor/acoustic/stop` - Stop acoustic sensor recording
- `POST /sensor/acoustic/pause` - Pause acoustic sensor recording
- `GET /sensor/acoustic/state` - Get acoustic sensor recording state
- `GET /sensor/acoustic/info` - Get acoustic sensor information
- `GET /sensor/acoustic/config` - Get acoustic sensor configuration
- `POST /sensor/acoustic/config` - Set acoustic sensor configuration

## Development

### Running Tests

Run the unit tests with:

```bash
python -m unittest discover -s UnitTests
```

### Hardware Access

For hardware access (e.g., cameras, sensors), specify the device path in the .env file:

```
CAMERA_DEVICE=/dev/video0  # Replace with your actual camera device
```

## License

This project is licensed under the MIT License.

## Contributors

- David Michalica, Team 1
