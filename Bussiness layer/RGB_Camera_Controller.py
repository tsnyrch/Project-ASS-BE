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
    
    def __init__(self):
        # Inicializace kamery
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()
        
        # Nastavení parametrů kamery
        self.camera.Width.Value = 1920
        self.camera.Height.Value = 1080
        self.camera.PixelFormat = "RGB8"

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
         
    def capture_image(self):
        # Získání snímku z kamery
        img = self.camera.GrabOne(1000)  # Timeout 1000 ms
        if img.GrabSucceeded():
            # Konverze na OpenCV formát
            image = img.Array
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            return image
        else:
            print("Chyba při získávání snímku.")
            return None
        
    def capture_image(self, count = 100):
        # count == numberOfImagesToGrab
        self.camera.StartGrabbingMax(count)

        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                # Access the image data.
                print("SizeX: ", grabResult.Width)
                print("SizeY: ", grabResult.Height)
                img = grabResult.Array
                print("Gray value of first pixel: ", img[0, 0])

        
    def release_camera(self):
        # Uvolnění kamery
        self.camera.Close()

# Příklad použití třídy
if __name__ == "__main__":
    camera_controller = RGB_Camera_Controller()
    while True:
        # Získání snímku
        frame = camera_controller.capture_image()
        if frame is not None:
            # Zobrazit snímek
            cv2.imshow("RGB Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  # Ukončení smyčky po stisku klávesy 'q'
    camera_controller.release_camera()
    cv2.destroyAllWindows()