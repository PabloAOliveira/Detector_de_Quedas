import time
import cv2
import serial
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
        self.fall_alert_sent = False  

        try:
            self.serial_port = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            time.sleep(2) 
            print("[INFO] Conectado ao Arduino via Serial.")
        except Exception as e:
            print(f"[ERRO] Não foi possível conectar ao Arduino: {e}")
            self.serial_port = None

    def enviar_para_arduino(self, comando):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(comando.encode())
                print(f"[DEBUG] Comando enviado ao Arduino: {comando}")
            except Exception as e:
                print(f"[ERRO] Falha ao enviar comando: {e}")

    def run(self):
        print("Iniciando monitoramento de quedas. Pressione 'q' para sair.")
        try:
            while True:
                frame = self.camera_service.get_frame()
                if frame is None:
                    print("[WARN] Frame vazio, tentando novamente...")
                    time.sleep(0.1)
                    continue

                landmarks = self.pose_detector.detect(frame)
                fallen = self.fall_detection_service.is_fallen(landmarks)
                self.person.is_fallen = fallen

                if fallen and not self.fall_alert_sent:
                    print(f"[ALERTA] {self.person.name} pode ter caído!")
                    self.enviar_para_arduino('1')
                    self.fall_alert_sent = True

                if not fallen:
                    self.fall_alert_sent = False 

                self.pose_detector.draw_landmarks(frame)
                cv2.imshow("Monitoramento de Queda", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                time.sleep(0.05)
        except KeyboardInterrupt:
            print("\n[INFO] Interrompido pelo usuário")
        finally:
            self.camera_service.close_camera()
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
            cv2.destroyAllWindows()
            print("[INFO] Recursos liberados com sucesso.")
