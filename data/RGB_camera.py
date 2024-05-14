from typing import Literal

class RGB_Camera_Start:

    def __init__(obj:object):
        path = obj.path
        name = obj.name
        count = obj.count
        quality = obj.quality
        image_format = obj.imae_format

    path:str
    name:str
    count:int = 1
    quality:int = 100
    image_format: Literal['bmp', 'tiff', 'jpeg', 'png', 'raw'] = 'png'
    