################################################
## Project: ASS/NSS API 
## Author: David Michalica, Team 1
## Date: 2024
## 
## Documentation: https://docs.alliedvision.com/Vimba_X/VmbC_Function_Reference/index.html
#################################################

#import cv2
#import numpy as np
#from mvIMPACT import acquire

# Implementace rozhraní pro multispektrální kameru
class Multispectral_Camera_Controller:
    
    def __init__(self):
        # Inicializace systému kamery
#        self.system = acquire.DeviceManager()
  #      self.system.updateDeviceList()
 #       self.device = self.system.getDevice(0)

        # Otevření komunikace s kamerou
  #      self.device.open()
  #      self.function_interface = self.device.getRemoteControl()
        
   # def acquire_image(self):
        
        # Získání snímku z kamery
    #    try:
    #        request = self.function_interface.requestSingle()
    #        if request.isOK:
    #            img_data = np.array(request.getBuffer())
    #            img_data = img_data.reshape((request.imageHeight(), request.imageWidth()))
    #            img_data = cv2.cvtColor(img_data, cv2.COLOR_GRAY2BGR)  # Pokud je jednobarevný
    #            return img_data
    #        else:
    #            print("Chyba při požadování snímku.")
    #            return None
    #    except Exception as e:
    #        print("Chyba při získávání snímku:", e)
    #        return None
    #    
   # def save_image(self, image, filename):
        # Uložení snímku na disk
   #     try:
   #         cv2.imwrite(filename, image)
   #         print("Snímek uložen jako", filename)
   #     except Exception as e:
   #         print("Chyba při ukládání snímku:", e)
   #     
   # def release_camera(self):
   #     # Uvolnění kamery
   #     self.device.close()

# Příklad použití třídy
if __name__ == "__main__":
    camera_controller = Multispectral_Camera_Controller()
    
    # Získání a zobrazení snímku
    image = camera_controller.acquire_image()
    if image is not None:
        cv2.imshow("Multispektrální kamera", image)
        cv2.waitKey(0)
        
        # Uložení snímku
        camera_controller.save_image(image, "multispectral_image.png")
        
    camera_controller.release_camera()
    cv2.destroyAllWindows()
