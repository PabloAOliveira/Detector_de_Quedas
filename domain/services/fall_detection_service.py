import math

class FallDetectionService:
    def __init__(self, angle_threshold=30, height_threshold=0.3):     
        #:param angle_threshold: Ângulo em graus para considerar como queda.
        #:param height_threshold: Diferença de altura relativa entre ombro e quadril
        self.angle_threshold = angle_threshold
        self.height_threshold = height_threshold

    def calculate_angle_from_vertical(self, p1, p2):
        delta_x = p2[0] - p1[0]
        delta_y = p2[1] - p1[1]
        
        angle_horizontal = math.degrees(math.atan2(delta_y, delta_x))
         
        angle_vertical = abs(90 - abs(angle_horizontal))
        
        return angle_vertical

    def calculate_height_difference(self, shoulder, hip):
        #:param shoulder: (x, y) do ombro
        #:param hip: (x, y) do quadril
        return abs(shoulder[1] - hip[1])

    def is_fallen(self, landmarks: dict) -> bool:
        #:param landmarks: dicionário com pontos relevantes
        left_shoulder = landmarks.get("left_shoulder")
        left_hip = landmarks.get("left_hip")

        if not left_shoulder or not left_hip:
            print("[WARN] Pontos insuficientes para avaliar queda.")
            return False

        # Critério 1: Ângulo do corpo em relação à vertical
        angle = self.calculate_angle_from_vertical(left_shoulder, left_hip)
        
        # Critério 2: Diferença de altura entre ombro e quadril
        height_diff = self.calculate_height_difference(left_shoulder, left_hip)
        
        print(f"[INFO] Ângulo vertical: {angle:.1f}°, Diff altura: {height_diff:.3f}")

        # Detecção de queda baseada em múltiplos critérios
        fall_detected = False
        
        if angle > (90 - self.angle_threshold):
            fall_detected = True
            print(f"[ALERT] Corpo muito horizontal! Ângulo: {angle:.1f}°")
        
        # Se a diferença de altura é muito pequena (pessoa deitada)
        elif height_diff < self.height_threshold:
            fall_detected = True
            print(f"[ALERT] Pessoa possivelmente deitada! Diff altura: {height_diff:.3f}")

        return fall_detected