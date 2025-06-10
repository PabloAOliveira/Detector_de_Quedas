import cv2
import time

class CameraService:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None

    def open_camera(self):
        print("[INFO] Abrindo câmera...")
        
        # Para Raspberry Pi Camera
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
            if self.cap.isOpened():
                # Aguarda um pouco para a câmera inicializar
                time.sleep(2)  # Aumentado para 2 segundos
                
                # Testa se consegue capturar um frame
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    print(f"[INFO] Câmera funcionando!")
                    # Configura resolução para melhor performance
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    self.cap.set(cv2.CAP_PROP_FPS, 30)
                    return
                else:
                    print("[WARN] Câmera abriu mas não captura frames")
                    self.cap.release()
            else:
                print("[WARN] Não foi possível abrir a câmera")
                if self.cap:
                    self.cap.release()
                    
        except Exception as e:
            print(f"[ERRO] Erro ao abrir câmera: {str(e)}")
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