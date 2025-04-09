"""
Data models for RGB camera operations.

This module contains data model classes for RGB camera operations,
providing proper validation and data structure for camera requests.
"""

from typing import Literal, Optional
from dataclasses import dataclass


@dataclass
class RGB_Camera_Config:
    """
    Configuration for RGB camera operations.
    
    This class defines the data structure for RGB camera capture requests,
    ensuring proper validation and typing.
    
    Attributes:
        path (str): Directory path where to save the image
        name (str): Name of the image file (without extension)
        count (int, optional): Number of images to capture. Defaults to 1.
        quality (int): Image quality (0-100). Defaults to 100.
        image_format (str): Format of the saved image. Defaults to 'png'.
    """
    
    path: str
    name: str
    count: int = 1
    quality: int = 100
    image_format: Literal["bmp", "tiff", "jpeg", "png", "raw"] = "png"
    
    def __post_init__(self):
        """
        Validate configuration after initialization.
        
        Raises:
            ValueError: If any of the parameters are invalid
        """
        # Validate path
        if not isinstance(self.path, str):
            raise ValueError("Path must be a string")
            
        # Validate name
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Name must be a non-empty string")
            
        # Validate count
        if not isinstance(self.count, int) or self.count < 1:
            raise ValueError("Count must be a positive integer")
            
        # Validate quality
        if not isinstance(self.quality, int) or not (0 <= self.quality <= 100):
            raise ValueError("Quality must be an integer between 0 and 100")
            
        # Validate image_format
        valid_formats = ["bmp", "tiff", "jpeg", "png", "raw"]
        if self.image_format not in valid_formats:
            raise ValueError(f"Image format must be one of: {', '.join(valid_formats)}")
            

@dataclass
class RGB_Camera_Response:
    """
    Response object for RGB camera operations.
    
    This class defines the data structure for RGB camera capture responses.
    
    Attributes:
        success (bool): Whether the operation was successful
        files (list): List of captured file paths
        count (int): Number of successfully captured images
        path (str): Directory path where images were saved
        format (str): Format of the saved images
        error (str, optional): Error message if operation failed
    """
    
    success: bool
    files: list
    count: int
    path: str
    format: str
    error: Optional[str] = None
    