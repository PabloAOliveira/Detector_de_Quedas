from picamera2 import Picamera2
import cv2
import time

class CameraService:
    def __init__(self):
        self.picam2 = None

    def open_camera(self):
        print("[INFO] Inicializando câmera com picamera2...")
        try:
            self.picam2 = Picamera2()
            self.picam2.preview_configuration.main.size = (640, 480)
            self.picam2.preview_configuration.main.format = "RGB888"
            self.picam2.configure("preview")
            self.picam2.start()
            time.sleep(2) 
            print("[INFO] Câmera iniciada com sucesso!")
        except Exception as e:
            raise Exception(f"[ERRO] Falha ao iniciar câmera: {str(e)}")

    def get_frame(self):
        if not self.picam2:
            raise Exception("[ERRO] Câmera não iniciada.")
        frame = self.picam2.capture_array()
        if frame is None or frame.size == 0:
            print("[WARN] Frame inválido.")
            return None
        print(f"[DEBUG] Frame capturado: {frame.shape}")
        return frame

    def close_camera(self):
        if self.picam2:
            self.picam2.close()
            print("[INFO] Câmera encerrada com sucesso.")
