import pygame
import os

class ButtonSound:
    _sound = None
    _volume = 0.5
    _sound_path = os.path.join("Source_files", "Assets", "Sounds", "bouton.mp3")

    @classmethod
    def play(cls, volume=None):
        if cls._sound is None:
            try:
                cls._sound = pygame.mixer.Sound(cls._sound_path)
                cls._sound.set_volume(cls._volume)
            except Exception as e:
                print(f"Error loading button sound: {e}")
                return
        if volume is not None:
            cls._sound.set_volume(volume)
        cls._sound.play()

    @classmethod
    def set_volume(cls, volume):
        cls._volume = volume
        if cls._sound:
            cls._sound.set_volume(volume)
