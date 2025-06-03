import cv2
import time

class CameraService:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None

    def open_camera(self):
        print("[INFO] Abrindo câmera...")
        
        # Tenta diferentes índices de câmera
        for index in [0, 1, -1]:
            print(f"[INFO] Tentando câmera {index}...")
            self.cap = cv2.VideoCapture(index)
            
            if self.cap.isOpened():
                # Aguarda um pouco para a câmera inicializar
                time.sleep(1)
                
                # Testa se consegue capturar um frame
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    print(f"[INFO] Câmera {index} funcionando!")
                    # Configura resolução para melhor performance
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    self.cap.set(cv2.CAP_PROP_FPS, 30)
                    return
                else:
                    print(f"[WARN] Câmera {index} abriu mas não captura frames")
                    self.cap.release()
            else:
                print(f"[WARN] Não foi possível abrir câmera {index}")
                if self.cap:
                    self.cap.release()
        
        raise Exception("[ERRO] Nenhuma câmera funcional encontrada.")

    def get_frame(self):
        if self.cap is None or not self.cap.isOpened():
            raise Exception("[ERRO] Câmera não iniciada ou fechada.")

        ret, frame = self.cap.read()
        if not ret:
            print("[WARN] ret=False - câmera não retornou frame")
            return None
        
        if frame is None:
            print("[WARN] Frame é None")
            return None
            
        if frame.size == 0:
            print("[WARN] Frame vazio (size=0)")
            return None
            
        print(f"[DEBUG] Frame capturado: {frame.shape}")
        return frame

    def close_camera(self):
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
            print("[INFO] Câmera fechada com sucesso.")