import pygame
import random
import os
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import database
from pydub import AudioSegment
from pydub.playback import play

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.playlists = {}
        self.current_playlist_name = "Default"
        self.playlists[self.current_playlist_name] = []
        self.current_index = 0
        self.playing = False
        self.paused = False
        self.shuffle = False
        self.repeat = False
        self.song_length = 0
        self.current_audio_segment = None  # Add this attribute
        self.load_songs_from_db()

    def load_songs_from_db(self):
        songs = database.get_all_songs()
        for title, artist, file_path in songs:
            self.add_songs([file_path])

    def add_songs(self, songs):
        playlist = self.playlists[self.current_playlist_name]
        for song in songs:
            if song not in playlist:
                playlist.append(song)
                title = os.path.basename(song)
                artist = "Unknown Artist"
                database.add_song(title, artist, song)

    def load_current_song(self):
        playlist = self.playlists[self.current_playlist_name]
        if not playlist:
            return None
        song = playlist[self.current_index]
        if song.endswith('.mp3'):
            pygame.mixer.music.load(song)
            audio = MP3(song)
            self.song_length = audio.info.length
        elif song.endswith('.mp4'):
            self.current_audio_segment = AudioSegment.from_file(song, format="mp4")
            self.song_length = len(self.current_audio_segment) / 1000.0  # Convert to seconds
        else:
            self.song_length = 0
        return song

    def play(self):
        song = self.load_current_song()
        if song:
            if song.endswith('.mp3'):
                pygame.mixer.music.play()
            elif song.endswith('.mp4'):
                play(self.current_audio_segment)
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
            self.current_index = 0
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

    def remove_song(self, song_index):
        playlist = self.playlists[self.current_playlist_name]
        if 0 <= song_index < len(playlist):
            removed_song = playlist.pop(song_index)
            database.remove_song(removed_song)
            if self.current_index >= len(playlist):
                self.current_index = 0
            return removed_song
        return None
