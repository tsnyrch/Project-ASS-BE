################################################
## Project: ASS/NSS API 
## Author: David Michalica, Team 1
## Date: 2024
## 
## Documentation: https://github.com/basler/pypylon
#################################################

from pypylon import pylon
import cv2

class RGB_Camera_Controller:
    
    def __init__(self, cameraWith = 1920, cameraHeight = 1080, cameraFormat = "RGB8"):
        # Inicializace kamery
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()
        
        # Nastavení parametrů kamery
        self.camera.Width.Value = cameraWith
        self.camera.Height.Value = cameraHeight
        #self.camera.PixelFormat = cameraFormat
         
    def capture_image(self):
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
        
    def release_camera(self):
        # Uvolnění kamery
        self.camera.Close()

# Příklad použití třídy
if __name__ == "__main__":
    camera_controller = RGB_Camera_Controller()
    val = camera_controller.capture_image()
    print(val)