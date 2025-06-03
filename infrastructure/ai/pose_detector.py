import cv2
import mediapipe as mp

class PoseDetector:
    def __init__(self, detection_confidence=0.5, tracking_confidence=0.5):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.current_results = None 

    def detect(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.current_results = self.pose.process(image_rgb)

        landmarks = {}
        if self.current_results.pose_landmarks:
            h, w, c = frame.shape
            
            for id, lm in enumerate(self.current_results.pose_landmarks.landmark):
                # Converter coordenadas normalizadas para pixels
                x, y = int(lm.x * w), int(lm.y * h)
                
                if id == 11:  # Left shoulder
                    landmarks["left_shoulder"] = (lm.x, lm.y)  # Manter normalizado para cálculos
                elif id == 12:  # Right shoulder
                    landmarks["right_shoulder"] = (lm.x, lm.y)
                elif id == 23:  # Left hip
                    landmarks["left_hip"] = (lm.x, lm.y)
                elif id == 24:  # Right hip
                    landmarks["right_hip"] = (lm.x, lm.y)

        return landmarks

    def draw_landmarks(self, frame):
        # Desenhar os pontos da pose    
        if self.current_results and self.current_results.pose_landmarks:
            # Desenhar todas as conexões da pose
            self.mp_drawing.draw_landmarks(
                frame, 
                self.current_results.pose_landmarks, 
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
            
            # Destacar pontos importantes
            h, w, c = frame.shape
            important_points = [11, 12, 23, 24]  # Ombros e quadris
            
            for id, lm in enumerate(self.current_results.pose_landmarks.landmark):
                if id in important_points:
                    x, y = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (x, y), 8, (255, 255, 0), -1)  # Círculo amarelo