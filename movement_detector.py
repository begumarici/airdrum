import cv2
import mediapipe as mp
from sound_trigger import SoundTrigger 

class MovementDetector:
    def __init__(self):
        # Önceki pozisyonlar
        self.previous_right_wrist_y = None
        self.previous_left_wrist_y = None
        self.previous_left_toe_y = None

        # trigger hassasiyet eşikleri
        self.threshold = 0.02  # Snare 
        self.hihat_threshold = 0.01  # Hi-hat 
        self.bass_threshold = 0.05  # Sol ayak ucu (Bass kick)
        self.movement_threshold = 0.3  # Cymbal ve Crash 

        self.sound_trigger = SoundTrigger()  

        # Seslerin tekrarlanmasını önlemek için bayraklar
        self.snare_triggered = False
        self.hihat_triggered = False
        self.crash_triggered = False
        self.cymbal_triggered = False
        self.bass_kick_triggered = False

    def detect_movement(self, landmarks):
        right_hand_tip = landmarks.landmark[20]  # Sağ elin en uç kısmı
        left_hand_tip = landmarks.landmark[19]  # Sol elin en uç kısmı

        left_toe_tip = landmarks.landmark[31]  # Sol ayak ucu

        left_shoulder = landmarks.landmark[11]  # Sol omuz
        right_shoulder = landmarks.landmark[12]  # Sağ omuz
        
        left_hip = landmarks.landmark[23]  # Sol kalça
        right_hip = landmarks.landmark[24]  # Sağ kalça

        body_center_x = (left_shoulder.x + right_shoulder.x) / 2
        hip_center_y = (left_hip.y + right_hip.y) / 2  # İki kalça arasındaki orta nokta
        mid_left_y = (left_shoulder.y + left_hip.y) / 2  # Sol omuz ve sol kalça arasındaki orta nokta

        # Snare tetiklemesi (Yukarıdan aşağıya hareket ile)
        if (
            self.previous_right_wrist_y is not None and 
            (right_hand_tip.y - self.previous_right_wrist_y) > self.threshold and
            abs(right_hand_tip.x - body_center_x) < 0.1 and
            abs(right_hand_tip.y - hip_center_y) < 0.05
        ):
            if not self.snare_triggered:
                self.sound_trigger.play_sound('snare')
                self.snare_triggered = True
        else:
            self.snare_triggered = False

        # Hi-hat tetiklemesi: Elin en uç kısmı omuz ve kalça arasında aşağıdan yukarıya hareketle tetiklenir
        if (
            self.previous_left_wrist_y is not None and 
            (left_hand_tip.y - self.previous_left_wrist_y) > self.hihat_threshold and  # Yukarıdan aşağı hareket kontrolü
            abs(left_hand_tip.x - body_center_x) < 0.1 and
            abs(left_hand_tip.y - hip_center_y) < 0.05
        ):
            if not self.hihat_triggered:

                
                self.sound_trigger.play_sound('hi_hat')
                self.hihat_triggered = True
        else:
            self.hihat_triggered = False

        # Bass-Kick tetiklenmesi: Sol ayak ucu yere değdiğinde 
        if self.previous_left_toe_y is not None and (left_toe_tip.y - self.previous_left_toe_y) > self.bass_threshold:
            if not self.bass_kick_triggered:
                self.sound_trigger.play_sound('bass_kick')
                self.bass_kick_triggered = True
        else:
            self.bass_kick_triggered = False

        # Crash tetiklenmesi : Sol kol vücudun sağ dışına doğru büyük hareket ederse 
        if left_hand_tip.x > right_shoulder.x + self.movement_threshold:
            if not self.crash_triggered:
                self.sound_trigger.play_sound('crash')
                self.crash_triggered = True
        else:
            self.crash_triggered = False

        # Cymbal tetiklenmesi: Sağ kol vücudun sol dışına doğru büyük hareket ederse 
        if right_hand_tip.x < left_shoulder.x - self.movement_threshold:
            if not self.cymbal_triggered:
                self.sound_trigger.play_sound('cymbal')
                self.cymbal_triggered = True
        else:
            self.cymbal_triggered = False

        # önceki pozisyonları güncelleme
        self.previous_right_wrist_y = right_hand_tip.y
        self.previous_left_wrist_y = left_hand_tip.y
        self.previous_left_toe_y = left_toe_tip.y
