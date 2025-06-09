import time
import cv2  
from infrastructure.camera.camera_service import CameraService
from infrastructure.ai.pose_detector import PoseDetector
from domain.services.fall_detection_service import FallDetectionService
from domain.entities.person import Person

class MonitorFallUseCase:
    def __init__(self):
        self.camera_service = CameraService()
        self.camera_service.open_camera()  
        self.pose_detector = PoseDetector()
        self.fall_detection_service = FallDetectionService()

        self.person = Person(id="1234", name="José")

    def run(self):
        print("Iniciando monitoramento de quedas. Pressione 'q' para sair.")
        try:
            while True:
                try:
                    frame = self.camera_service.get_frame()
                    if frame is None:
                        print("[WARN] Frame vazio, tentando novamente...")
                        time.sleep(0.1)
                        continue

                    landmarks = self.pose_detector.detect(frame)
                    fallen = self.fall_detection_service.is_fallen(landmarks)
                    self.person.is_fallen = fallen

                    if fallen:
                        print(f"[ALERTA] {self.person.name} pode ter caído!")

                    self.pose_detector.draw_landmarks(frame)

                    cv2.imshow("Monitoramento de Queda", frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                    time.sleep(0.05)  # controla o tempo para reduzir uso de CPU
                
                except Exception as e:
                    print(f"[ERROR] Erro durante captura: {e}")
                    continue

        except KeyboardInterrupt:
            print("\n[INFO] Interrompido pelo usuário")
        finally:
            self.camera_service.close_camera()  
            cv2.destroyAllWindows()