import pygame, sys
import cv2
import numpy as np
from pygame.locals import *
from settings import *
import time


class Cutscene():
    def __init__(self, game):
        print("Initializing Cutscene...")
        self.game = game
        self.screen = game.screen
        self.next_scene_name = None
        self.BLACK = (0, 0, 0)
        
        # Initialize audio
        pygame.mixer.init()
        
        # List of videos to play in sequence with their settings
        self.videos = [
            {
                "path": "assets/backgrounds/intro.mp4",
                "audio_path": None,  # No audio for intro
                "use_normal_speed": False,  # Intro video plays at original speed
                "has_audio": False
            },
            {
                "path": "assets/backgrounds/story.mp4",
                "audio_path": "assets/backgrounds/story.mp3",  # MP3 audio file
                "use_normal_speed": True,   # Story video plays at normal speed with audio
                "has_audio": True
            }
        ]
        self.current_video_index = 0
        self.last_frame_time = 0
        self.video_start_time = 0
        self.load_next_video()

    def load_next_video(self):
        try:
            if hasattr(self, 'cap'):
                self.cap.release()
            
            if self.current_video_index >= len(self.videos):
                print("All videos finished, transitioning to gameplay...")
                self.next_scene_name = "GAMEPLAY"
                return

            current_video = self.videos[self.current_video_index]
            print(f"Loading video {self.current_video_index + 1}/{len(self.videos)}: {current_video['path']}")
            self.cap = cv2.VideoCapture(current_video['path'])
            
            if not self.cap.isOpened():
                print(f"Error: Could not open video file: {current_video['path']}")
                self.next_scene_name = "GAMEPLAY"
                return
                
            print("Video loaded successfully")
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.current_frame = 0
            self.last_frame_time = time.time()
            self.video_start_time = time.time()
            
            # Load and play audio only for videos that should have audio
            if current_video['has_audio'] and current_video['audio_path']:
                try:
                    pygame.mixer.music.load(current_video['audio_path'])
                    pygame.mixer.music.play()
                except Exception as e:
                    print(f"Error playing audio: {e}")
            
        except Exception as e:
            print(f"Error loading video: {e}")
            self.next_scene_name = "GAMEPLAY"

    def handle_events(self, events):
        if self.next_scene_name: # If scene transition is pending, do nothing
            return
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN: # Skip video
                    print("Skipping current video...")
                    if self.videos[self.current_video_index]['has_audio']:
                        pygame.mixer.music.stop()
                    self.current_video_index += 1
                    self.load_next_video()

    def update(self):
        # If scene transition is pending, no need to process video
        if self.next_scene_name:
            return

        try:
            current_video = self.videos[self.current_video_index]
            
            # Only check frame timing for videos that should play at normal speed
            if current_video['use_normal_speed']:
                current_time = time.time()
                frame_delay = 1.0 / self.fps
                if current_time - self.last_frame_time < frame_delay:
                    return
                self.last_frame_time = current_time

            ret, frame = self.cap.read()
            if not ret:
                print(f"Video {self.current_video_index + 1} ended")
                if current_video['has_audio']:
                    pygame.mixer.music.stop()
                self.current_video_index += 1
                self.load_next_video()
                return
            
            # Convert frame from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert to pygame surface
            self.current_video_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.current_frame += 1
            
        except Exception as e:
            print(f"Error during video playback: {e}")
            self.next_scene_name = "GAMEPLAY"

    def draw(self):
        self.screen.fill(self.BLACK) # Always fill the screen with black first

        # If scene transition is pending, just clear the screen and force an update, then return
        if self.next_scene_name:
            pygame.display.update() # Force update to clear any lingering frames
            return

        # Only draw if we have a frame
        if hasattr(self, 'current_video_frame') and self.current_video_frame:
            try:
                scaled_frame = pygame.transform.scale(self.current_video_frame, (WIDTH, HEIGHT))
                self.screen.blit(scaled_frame, (0, 0))
            except Exception as e:
                print(f"Error drawing video frame: {e}")
                self.next_scene_name = "GAMEPLAY"
        # pygame.display.flip() is handled by the main game loop
        