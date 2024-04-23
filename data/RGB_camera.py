from typing import Literal

class RGB_Camera_Start:
    path:str
    name:str
    count:int = 1
    quality:int = 100
    image_format: Literal['bmp', 'tiff', 'jpeg', 'png', 'raw'] = 'png'
    