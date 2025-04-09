"""
General unit tests for the ASS/NSS API.

This module contains the basic tests for the API functionality.
"""

import json
import os
import sys
import unittest

# Add parent directory to path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from config import TestingConfig
from data.RGB_camera import RGB_Camera_Config


class GeneralTestCase(unittest.TestCase):
    """Test case for general API functionality."""

    def setUp(self):
        """Set up test client and configure app for testing."""
        app.config.from_object(TestingConfig)
        self.app = app.test_client()
        self.app.testing = True

    def test_root_endpoint(self):
        """Test the root endpoint returns a greeting."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, World!", response.data)

    def test_rgb_camera_config_validation(self):
        """Test RGB camera configuration validation."""
        # Test valid config
        valid_config = RGB_Camera_Config(
            path="./test/", name="test_image", count=2, quality=90, image_format="png"
        )
        self.assertEqual(valid_config.path, "./test/")
        self.assertEqual(valid_config.name, "test_image")
        self.assertEqual(valid_config.count, 2)
        self.assertEqual(valid_config.quality, 90)
        self.assertEqual(valid_config.image_format, "png")

        # Test invalid quality
        with self.assertRaises(ValueError):
            RGB_Camera_Config(
                path="./test/",
                name="test_image",
                quality=101,  # Quality should be 0-100
            )

        # Test invalid count
        with self.assertRaises(ValueError):
            RGB_Camera_Config(
                path="./test/", name="test_image", count=0  # Count should be positive
            )

        # Test invalid format
        with self.assertRaises(ValueError):
            RGB_Camera_Config(
                path="./test/",
                name="test_image",
                image_format="invalid",  # Format should be one of the allowed values
            )


class APIEndpointTestCase(unittest.TestCase):
    """Test case for API endpoints."""

    def setUp(self):
        """Set up test client and configure app for testing."""
        app.config.from_object(TestingConfig)
        self.app = app.test_client()
        self.app.testing = True

    def test_rgb_config_endpoint(self):
        """Test the RGB camera config endpoint (mocked)."""
        # This is a partial test as it can't connect to actual hardware during tests
        response = self.app.get("/sensor/rgb/config")
        # Expecting error because no real camera in test environment
        self.assertNotEqual(response.status_code, 200)

    def test_rgb_start_endpoint_validation(self):
        """Test validation for RGB camera start endpoint."""
        # Missing required fields
        response = self.app.post(
            "/sensor/rgb/start",
            json={"path": "./test/"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertIn("Missing required fields", data["error"])


if __name__ == "__main__":
    unittest.main()
