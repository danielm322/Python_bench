"""
Audio manager for Tetris Android.

Handles background music and sound effects using Kivy's audio system.
"""

from kivy.core.audio import SoundLoader
from kivy.utils import platform
import os


class AudioManager:
    """
    Manages all game audio including music and sound effects.
    
    Attributes:
        music: Background music Sound object
        sounds: Dictionary of sound effect Sound objects
        music_enabled: Whether music is enabled
        sfx_enabled: Whether sound effects are enabled
    """
    
    def __init__(self):
        """Initialize the audio manager."""
        self.music = None
        self.sounds = {}
        self.music_enabled = True
        self.sfx_enabled = True
        self.music_volume = 0.3  # Lower volume for background music
        self.sfx_volume = 0.5
        self.music_file = None
        self.initialized = False
        
        # Don't initialize audio immediately to avoid blocking startup
        # Audio will be initialized on first use
    
    def _init_sounds(self):
        """Initialize sound effects with generated tones."""
        try:
            from sound_generator import create_game_sounds
            self.sounds = create_game_sounds()
        except Exception as e:
            print(f"Could not initialize sounds: {e}")
            # Fallback to empty sounds
            self.sounds = {
                'move': None,
                'rotate': None,
                'drop': None,
                'clear': None,
                'tetris': None,
                'game_over': None,
            }
    
    def _load_pregenerated_sounds(self):
        """Load pre-generated sound files from assets directory."""
        import os
        
        sound_dir = os.path.join(os.path.dirname(__file__), 'assets', 'sounds')
        
        if not os.path.exists(sound_dir):
            print(f"Sound directory not found: {sound_dir}")
            return
        
        # Load each sound file
        for sound_name in ['move', 'rotate', 'drop', 'clear', 'tetris', 'game_over']:
            sound_path = os.path.join(sound_dir, f'{sound_name}.wav')
            if os.path.exists(sound_path):
                sound = SoundLoader.load(sound_path)
                if sound:
                    self.sounds[sound_name] = sound
                    print(f"Loaded {sound_name}.wav")
                else:
                    print(f"Failed to load {sound_name}.wav")
            else:
                print(f"Sound file not found: {sound_path}")
        
        # Load background music if available
        music_path = os.path.join(os.path.dirname(__file__), 'assets', 'tetris_music.wav')
        if os.path.exists(music_path):
            self.music_file = music_path
            print(f"Music file found: {music_path}")
        else:
            print("No background music file found")
    
    def ensure_initialized(self):
        """Ensure audio is initialized (lazy initialization)."""
        if not self.initialized:
            try:
                print("Loading pre-generated audio files...")
                self._load_pregenerated_sounds()
                self.initialized = True
                print("Audio loaded successfully")
            except Exception as e:
                print(f"Could not load audio: {e}")
                self.initialized = True
            return
    
    def play_sound(self, sound_name: str):
        """
        Play a sound effect.
        
        Args:
            sound_name: Name of the sound to play
        """
        self.ensure_initialized()
        
        if not self.sfx_enabled:
            return
        
        sound = self.sounds.get(sound_name)
        if sound:
            sound.volume = self.sfx_volume
            sound.play()
    
    def play_music(self, music_file: str = None):
        """
        Play background music.
        
        Args:
            music_file: Path to music file (optional)
        """
        self.ensure_initialized()
        
        if not self.music_enabled:
            return
        
        if self.music:
            self.music.stop()
        
        if music_file and os.path.exists(music_file):
            self.music = SoundLoader.load(music_file)
            if self.music:
                self.music.volume = self.music_volume
                self.music.loop = True
                self.music.play()
    
    def stop_music(self):
        """Stop background music."""
        if self.music:
            self.music.stop()
    
    def pause_music(self):
        """Pause background music."""
        if self.music and self.music.state == 'play':
            self.music.stop()
    
    def resume_music(self):
        """Resume background music."""
        if self.music and self.music_enabled:
            self.music.play()
    
    def set_music_volume(self, volume: float):
        """
        Set music volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        if self.music:
            self.music.volume = self.music_volume
    
    def set_sfx_volume(self, volume: float):
        """
        Set sound effects volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def toggle_music(self):
        """Toggle music on/off."""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.resume_music()
        else:
            self.pause_music()
    
    def toggle_sfx(self):
        """Toggle sound effects on/off."""
        self.sfx_enabled = not self.sfx_enabled
