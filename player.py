import pygame
import random
from mutagen.mp3 import MP3

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        # Dictionary: playlist name -> list of song file paths.
        self.playlists = {}
        self.current_playlist_name = "Default"
        self.playlists[self.current_playlist_name] = []  # Create a default playlist.
        self.current_index = 0
        self.playing = False     # True when a song is playing.
        self.paused = False      # True when playback is paused.
        self.shuffle = False
        self.repeat = False      # True when repeat is enabled.
        self.song_length = 0     # Duration (in seconds) of the current song.

    def add_songs(self, songs):
        playlist = self.playlists[self.current_playlist_name]
        for song in songs:
            if song not in playlist:
                playlist.append(song)

    def load_current_song(self):
        playlist = self.playlists[self.current_playlist_name]
        if not playlist:
            return None
        song = playlist[self.current_index]
        pygame.mixer.music.load(song)
        try:
            audio = MP3(song)
            self.song_length = audio.info.length
        except Exception:
            self.song_length = 0
        return song

    def play(self):
        song = self.load_current_song()
        if song:
            pygame.mixer.music.play()
            self.playing = True
            self.paused = False
        return song

    def pause(self):
        if self.playing:
            if not self.paused:
                pygame.mixer.music.pause()
                self.paused = True
            else:
                pygame.mixer.music.unpause()
                self.paused = False

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.paused = False

    def next_song(self):
        playlist = self.playlists[self.current_playlist_name]
        if not playlist:
            return None
        if self.shuffle:
            self.current_index = random.randint(0, len(playlist) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(playlist)
        
        if self.repeat and self.current_index == 0:
            self.current_index = 0  # Stay on the first song if repeat is enabled.
        return self.play()

    def prev_song(self):
        playlist = self.playlists[self.current_playlist_name]
        if not playlist:
            return None
        if self.shuffle:
            self.current_index = random.randint(0, len(playlist) - 1)
        else:
            self.current_index = (self.current_index - 1) % len(playlist)
        return self.play()

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle

    def toggle_repeat(self):
        self.repeat = not self.repeat

    def seek_to(self, pos):
        if self.playing:
            was_paused = self.paused
            pygame.mixer.music.stop()
            pygame.mixer.music.play(start=pos)
            if was_paused:
                pygame.mixer.music.pause()
