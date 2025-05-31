import pygame

class SoundTrigger:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)  
        pygame.mixer.init()
        self.hi_hat_sound = pygame.mixer.Sound('assets/Closed-Hi-Hat-1.wav')
        self.snare_sound = pygame.mixer.Sound('assets/Ensoniq-ESQ-1-Snare.wav')  
        self.cymbal_sound = pygame.mixer.Sound('assets/Ensoniq-SQ-1-Ride-Cymbal.wav')
        self.crash_sound = pygame.mixer.Sound('assets/Crash-Cymbal-1.wav')
        self.bass_kick_sound = pygame.mixer.Sound('assets/Bass-Drum-2.wav')  

    def play_sound(self, sound_name):
        if sound_name == "hi_hat":
            self.hi_hat_sound.play()
        elif sound_name == "snare": 
            self.snare_sound.play()
        elif sound_name == "cymbal":
            self.cymbal_sound.play()
        elif sound_name == "crash":
            self.crash_sound.play()
        elif sound_name == "bass_kick":  
            self.bass_kick_sound.play()
