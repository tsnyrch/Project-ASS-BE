import SensorController
import RGB_Camera_Controller
import MultiSpectral_Camera_Controller

class SensoreService:

    def __init__(self, SensorController, RGB_Camera_Controller, Multispectral_Camera_Controller):
        self.SensorController = SensorController
        self.RGB_Camera_Controller = RGB_Camera_Controller
        self.Multispectral_Camera_Controller = Multispectral_Camera_Controller

    def StartMesurement():
        try:
            time = self.SensorController.GetSystemTime("001")
            sensors = self.SensorController.GetSensors("001")
            config = self.SensorController.GetConfiguration("001")
            recording = self.SensorController.StartRecording("001")
            reader = self.SensorController.OpenFileReaderByName("001")
            reader_info = self.SensorController.GetFileReaderInfo("001")
            reader_data = self.SensorController.GetFileReaderData("001")
        except:
            print("Nastala chyba při zpracování náhrávání")
            return 
    
    def StopMesurement():
        time = self.SensorController.StopRecording("001")
        return 0

# Příklad použití třídy
if __name__ == "__main__":
    sensor = SensorController("192.168.0.196", 40999)
    Multispec = Multispectral_Camera_Controller()
    Rgb = RGB_Camera_Controller()

    sensoreService = SensoreService(sensor, Rgb, Multispec)