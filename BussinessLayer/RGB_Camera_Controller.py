################################################
## Project: ASS/NSS API
## Author: David Michalica, Team 1
## Date: 2024
##
## Documentation: https://github.com/basler/pypylon
#################################################

import logging
from typing import Any, Dict, List, Literal, Optional

from pypylon import pylon

# Set up logging
logger = logging.getLogger(__name__)


class RGB_Camera_Controller:
    """
    Controller for RGB camera operations using the Basler Pylon library.

    This class provides methods to connect to a Basler camera,
    configure it, and capture images in various formats.

    Attributes:
        save_functions (Dict): Mapping of image formats to Pylon image format constants
        camera_width (int): Width of the camera image in pixels
        camera_height (int): Height of the camera image in pixels
    """

    save_functions = {
        "png": pylon.ImageFileFormat_Png,
        "raw": pylon.ImageFileFormat_Raw,
        "tiff": pylon.ImageFileFormat_Tiff,
    }

    def __init__(
        self,
        camera_width: int = 1920,
        camera_height: int = 1080,
        camera_format: str = "RGB8",
    ):
        """
        Initialize the RGB Camera Controller.

        Args:
            camera_width (int, optional): Width of the camera image in pixels. Defaults to 1920.
            camera_height (int, optional): Height of the camera image in pixels. Defaults to 1080.
            camera_format (str, optional): Format of the camera image. Defaults to "RGB8".
        """
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.camera_format = camera_format
        self.camera = None
        logger.info(
            f"RGB_Camera_Controller initialized with resolution {camera_width}x{camera_height}"
        )

    def Connect(self) -> bool:
        """
        Initialize and connect to the camera.

        Returns:
            bool: True if connection was successful, False otherwise

        Raises:
            RuntimeError: If camera connection fails
        """
        try:
            # Initialize camera
            self.camera = pylon.InstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice()
            )
            self.camera.Open()

            # Set camera parameters
            self.camera.Width.Value = self.camera_width
            self.camera.Height.Value = self.camera_height

            logger.info("Camera connected successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to camera: {str(e)}")
            raise RuntimeError(f"Camera connection failed: {str(e)}")

    def acquire_image(self) -> Optional[Any]:
        """
        Acquire a single image from the camera.

        Returns:
            Optional[Any]: The acquired image as a numpy array, or None if acquisition failed

        Raises:
            RuntimeError: If the camera is not connected
        """
        if not self.camera:
            logger.error("Camera not connected. Call Connect() first.")
            raise RuntimeError("Camera not connected. Call Connect() first.")

        try:
            if self.camera.IsGrabbing():
                self.camera.StopGrabbing()

            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

            grab_result = self.camera.RetrieveResult(
                5000, pylon.TimeoutHandling_ThrowException
            )

            if grab_result.GrabSucceeded():
                image = grab_result.Array
                grab_result.Release()
                logger.info("Image acquired successfully")
                return image
            else:
                logger.error(
                    f"Image acquisition failed: {grab_result.ErrorDescription}"
                )
                grab_result.Release()
                return None
        except Exception as e:
            logger.error(f"Error acquiring image: {str(e)}")
            return None

    def capture_image(
        self,
        path: str,
        name: str,
        count: int = 1,
        quality: int = 100,
        image_format: Literal["tiff", "png", "raw"] = "png",
    ) -> Dict[str, Any]:
        """
        Capture and save images from the camera.

        Args:
            path (str): Directory path where to save the image
            name (str): Name of the image file (without extension)
            count (int, optional): Number of images to capture. Defaults to 1.
            quality (int, optional): Image quality (0-100). Defaults to 100.
            image_format (Literal["tiff", "png", "raw"], optional): Format of the saved image. Defaults to "png".

        Returns:
            Dict[str, Any]: Dictionary with status and file information

        Raises:
            ValueError: If an unsupported image format is specified
            RuntimeError: If the camera is not connected
        """
        if not self.camera:
            logger.error("Camera not connected. Call Connect() first.")
            raise RuntimeError("Camera not connected. Call Connect() first.")

        if image_format not in self.save_functions:
            logger.error(f"Unsupported image format: {image_format}")
            raise ValueError(
                f"Unsupported image format: {image_format}. Supported formats: {list(self.save_functions.keys())}"
            )

        result = {
            "success": False,
            "files": [],
            "count": 0,
            "path": path,
            "format": image_format,
        }

        try:
            img = pylon.PylonImage()
            self.camera.StartGrabbing()

            captured_count = 0
            for i in range(count):
                try:
                    with self.camera.RetrieveResult(2000) as result_obj:
                        if not result_obj.GrabSucceeded():
                            logger.warning(
                                f"Failed to grab image {i + 1}/{count}: {result_obj.ErrorDescription}"
                            )
                            continue

                        # Attach grab result buffer to prevent reuse for grabbing
                        img.AttachGrabResultBuffer(result_obj)

                        # Generate filename and determine format
                        filename = (
                            f"{path}{name}_{i + 1}.{image_format}"
                            if count > 1
                            else f"{path}{name}.{image_format}"
                        )
                        format_value = self.save_functions[image_format]

                        # Configure and save the image
                        ipo = pylon.ImagePersistenceOptions()
                        ipo.SetQuality(quality)
                        img.Save(format_value, filename, ipo)

                        result["files"].append(filename)
                        captured_count += 1

                        # Release image to make buffer available again
                        img.Release()
                except Exception as e:
                    logger.error(f"Error capturing image {i + 1}/{count}: {str(e)}")
                    continue

            self.camera.StopGrabbing()

            result["success"] = captured_count > 0
            result["count"] = captured_count

            logger.info(
                f"Captured {captured_count}/{count} images in {image_format} format"
            )
            return result
        except Exception as e:
            logger.error(f"Error in capture_image: {str(e)}")
            self.camera.StopGrabbing()
            raise
        finally:
            # Don't automatically close the camera - let the caller decide when to release
            pass

    def grab(self, count: int = 100) -> List[Dict[str, Any]]:
        """
        Demonstrate feature access by grabbing multiple images and analyzing them.

        Args:
            count (int, optional): Number of images to grab. Defaults to 100.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing image information

        Raises:
            RuntimeError: If the camera is not connected
        """
        if not self.camera:
            logger.error("Camera not connected. Call Connect() first.")
            raise RuntimeError("Camera not connected. Call Connect() first.")

        results = []
        try:
            # Demonstrate feature access
            new_width = self.camera.Width.GetValue() - self.camera.Width.GetInc()
            if new_width >= self.camera.Width.GetMin():
                self.camera.Width.SetValue(new_width)

            self.camera.StartGrabbingMax(count)

            while self.camera.IsGrabbing():
                grabResult = self.camera.RetrieveResult(
                    5000, pylon.TimeoutHandling_ThrowException
                )

                if grabResult.GrabSucceeded():
                    img = grabResult.Array
                    img_info = {
                        "width": grabResult.Width,
                        "height": grabResult.Height,
                        "first_pixel_value": int(img[0, 0]),
                    }
                    results.append(img_info)
                    logger.debug(f"Grabbed image: {img_info}")

                grabResult.Release()

            logger.info(f"Completed grabbing {len(results)} images")
            return results
        except Exception as e:
            logger.error(f"Error in grab method: {str(e)}")
            raise
        finally:
            if self.camera and self.camera.IsGrabbing():
                self.camera.StopGrabbing()

    def release_camera(self) -> None:
        """
        Release camera resources.

        This method should be called when done with the camera to properly release resources.
        """
        try:
            if self.camera:
                if self.camera.IsGrabbing():
                    self.camera.StopGrabbing()
                self.camera.Close()
                logger.info("Camera released successfully")
        except Exception as e:
            logger.error(f"Error releasing camera: {str(e)}")
            raise


# Example usage (only run if this file is executed directly)
if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(level=logging.INFO)

    try:
        camera_controller = RGB_Camera_Controller()
        camera_controller.Connect()
        result = camera_controller.capture_image("./", "test_image")
        print(f"Capture result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if camera_controller:
            camera_controller.release_camera()
