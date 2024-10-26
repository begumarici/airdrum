import cv2
import mediapipe as mp
from sound_trigger import SoundTrigger 

class MovementDetector:
    def __init__(self):
        self.previous_right_wrist_y = None
        self.previous_left_wrist_y = None  # Sol bilek için
        self.previous_left_toe_y = None  # Sol ayak ucu için
        self.left_toe_up = False  # Sol ayak ucunun kalktığını izlemek için
        self.threshold = 0.01  # Hareket algılama eşiği (snare ve hi-hat için daha hassas)
        self.bass_threshold = 0.05  # Sol ayak ucu için daha düşük hassasiyet
        self.movement_threshold = 0.3  # Cymbal ve Crash için daha büyük hareket eşiği
        self.sound_trigger = SoundTrigger()  

        # Seslerin tekrarlanmasını önlemek için tetikleme bayrakları
        self.snare_triggered = False
        self.hihat_triggered = False
        self.crash_triggered = False
        self.cymbal_triggered = False
        self.bass_kick_triggered = False

    def detect_movement(self, landmarks):
        # Sağ ve sol bilek ve ayak ucu
        right_wrist = landmarks.landmark[16]  # Sağ bilek
        left_wrist = landmarks.landmark[15]  # Sol bilek
        left_toe_tip = landmarks.landmark[31]  # Sol ayak ucu (ayak parmak ucu)
        left_shoulder = landmarks.landmark[11]  # Sol omuz
        right_shoulder = landmarks.landmark[12]  # Sağ omuz
        body_center_x = (left_shoulder.x + right_shoulder.x) / 2
        body_lower_y = (left_shoulder.y + right_shoulder.y) / 2 + 0.2  # Gövdenin alt kısmı (göbek seviyesi)
        lower_left_body_y = left_shoulder.y + 0.3  # Sol alt gövde referans noktası

        # Snare tetiklemesi: Sağ bilek aşağı doğru hareket ettiğinde ve gövdenin alt kısmına yakınsa
        if self.previous_right_wrist_y is not None and (self.previous_right_wrist_y - right_wrist.y) > self.threshold:
            if right_wrist.x < body_center_x and right_wrist.y > body_lower_y:  # Sağ bilek gövde merkezine yakın
                if not self.snare_triggered:
                    self.sound_trigger.play_sound('snare')
                    self.snare_triggered = True
            else:
                self.snare_triggered = False

        # Hi-hat tetiklemesi: Sol bilek gövdenin sağ tarafına doğru hareket ettiğinde ve daha hassas tetikleme
        if self.previous_left_wrist_y is not None and (self.previous_left_wrist_y - left_wrist.y) > self.threshold:
            if left_wrist.x > body_center_x:  # Sol bilek vücudun sağ tarafına hareket ettiğinde
                if not self.hihat_triggered:
                    self.sound_trigger.play_sound('hi_hat')
                    self.hihat_triggered = True
            else:
                self.hihat_triggered = False

        # Sol ayak ucu yere değdiğinde (bass kick tetikleme)
        if self.previous_left_toe_y is not None and (left_toe_tip.y - self.previous_left_toe_y) > self.bass_threshold:
            if not self.bass_kick_triggered:
                self.sound_trigger.play_sound('bass_kick')
                self.bass_kick_triggered = True
        else:
            self.bass_kick_triggered = False  # Yeniden tetiklenmeye hazır

        # Sol kol vücudun sağ dışına doğru büyük hareket ederse (crash tetikleme)
        if left_wrist.x > right_shoulder.x + self.movement_threshold:
            if not self.crash_triggered:
                self.sound_trigger.play_sound('crash')
                self.crash_triggered = True
        else:
            self.crash_triggered = False

        # Sağ kol vücudun sol dışına doğru büyük hareket ederse (cymbal tetikleme)
        if right_wrist.x < left_shoulder.x - self.movement_threshold:
            if not self.cymbal_triggered:
                self.sound_trigger.play_sound('cymbal')
                self.cymbal_triggered = True
        else:
            self.cymbal_triggered = False

        # Güncellenen bilek ve ayak pozisyonları
        self.previous_right_wrist_y = right_wrist.y
        self.previous_left_wrist_y = left_wrist.y
        self.previous_left_toe_y = left_toe_tip.y
