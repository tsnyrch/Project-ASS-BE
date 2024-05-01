################################################
## Project: ASS/NSS API 
## Author: David Michalica, Team 1
## Date: 2024
## 
## Documentation: https://github.com/basler/pypylon
#################################################

from pypylon import pylon
from typing import Literal

class RGB_Camera_Controller:
    
    save_functions = {
        'png': pylon.ImageFileFormat_Png,
        'raw': pylon.ImageFileFormat_Raw,
        #'jpeg': pylon.ImageFileFormat_Jpeg,
        'tiff': pylon.ImageFileFormat_Tiff,
        #'bmp': pylon.ImageFileFormat_Bmp,
    }

    def __init__(self, cameraWith = 1920, cameraHeight = 1080, cameraFormat = "RGB8"):
 
        # Nastavení parametrů kamery
        self.camera.Width.Value = cameraWith
        self.camera.Height.Value = cameraHeight
        self.camera.PixelFormat = cameraFormat

    def Connect(self):
        # Inicializace kamery
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()

    def acquire_image(self):
        try:
            if self.camera.IsGrabbing():
                self.camera.StopGrabbing()

            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

            grab_result = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grab_result.GrabSucceeded():
                image = grab_result.Array
                grab_result.Release()
                return image
            else:
                print("Chyba při získávání snímku.")
                return None
        except Exception as e:
            print("Chyba při získávání snímku:", e)
            return None
         
    def capture_image(self, path, name, count = 1, quality = 100, image_format: Literal['bmp', 'tiff', 'jpeg', 'png', 'raw'] = 'png' ):
        """
        This sample shows how grabbed images can be saved using pypylon only (no need to use openCV).
        https://github.com/basler/pypylon/blob/master/samples/save_image.py
        To take a photo, it is necessary to have a lens attached to the camera !!!

        Available image formats are     (depending on platform):
        - pylon.ImageFileFormat_Bmp    (Windows)
        - pylon.ImageFileFormat_Tiff   (Linux, Windows)
        - pylon.ImageFileFormat_Jpeg   (Windows)
        - pylon.ImageFileFormat_Png    (Linux, Windows)
        - pylon.ImageFileFormat_Raw    (Windows)
        """
        img = pylon.PylonImage()
        self.camera.StartGrabbing()

        for i in range(count):
            with self.camera.RetrieveResult(2000) as result:
    
                # Calling AttachGrabResultBuffer creates another reference to the
                # grab result buffer. This prevents the buffer's reuse for grabbing.
                img.AttachGrabResultBuffer(result)
                filename = path + name + "." + image_format
                format = self.save_functions[image_format]
    
                # The JPEG format that is used here supports adjusting the image
                # quality (100 -> best quality, 0 -> poor quality).
                ipo = pylon.ImagePersistenceOptions()
                ipo.SetQuality(quality)
                img.Save(format, filename)
    
                # In order to make it possible to reuse the grab result for grabbing
                # again, we have to release the image (effectively emptying the image object).
                img.Release()
 
        self.camera.StopGrabbing()
        self.camera.Close()

    def grab(self, count = 100):
    
        # demonstrate some feature access
        new_width = self.camera.Width.GetValue() - self.camera.Width.GetInc()
        if new_width >= self.camera.Width.GetMin():
            self.camera.Width.SetValue(new_width)
    
        numberOfImagesToGrab = count
        self.camera.StartGrabbingMax(numberOfImagesToGrab)
    
        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    
            if grabResult.GrabSucceeded():
                # Access the image data.
                print("SizeX: ", grabResult.Width)
                print("SizeY: ", grabResult.Height)
                img = grabResult.Array
                print("Gray value of first pixel: ", img[0, 0])
    
            grabResult.Release()
        self.camera.Close()


    def release_camera(self):
        # Uvolnění kamery
        self.camera.Close()

# Příklad použití třídy
if __name__ == "__main__":
    camera_controller = RGB_Camera_Controller()
    camera_controller.capture_image("", "pokus")