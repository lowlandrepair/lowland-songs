import tkinter as tk
import os
import pygame
from tkinter import filedialog, messagebox, simpledialog
from player import MusicPlayer
from components.sidebar import Sidebar
from components.main_content import MainContent
from components.bottom_controls import BottomControls
from styles.theme import *

# Consolidated UI Class
class LowlandUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lowland Music Player")
        self.root.geometry("1200x700")
        self.root.configure(bg=BG_COLOR)
        self.root.bind("<Right>", self.skip_forward)
        self.root.bind("<Left>", self.skip_backward)
        self.root.bind("<space>", lambda e: self.toggle_play_pause())
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.player = MusicPlayer()
        nav_commands = {
            "Home": self.show_home,
            "Search": self.show_search,
            "Your Library": self.show_library
        }
        self.sidebar = Sidebar(self.root, nav_commands)
        self.main_content = MainContent(self.root, self.player, self.play_song_by_index)
        play_callbacks = {
            'prev': self.prev_song,
            'toggle': self.toggle_play_pause,
            'next': self.next_song,
            'toggle_shuffle': self.toggle_shuffle,
            'toggle_repeat': self.toggle_repeat
        }
        self.bottom_controls = BottomControls(self.root, self.player, play_callbacks)
        self.show_home()

    def show_home(self):
        self.main_content.show_home()

    def show_search(self):
        self.main_content.show_search()

    def show_library(self):
        self.main_content.show_library(self.refresh_playlist_listbox)

    def refresh_playlist_listbox(self):
        if hasattr(self.main_content, 'playlist_listbox'):
            self.main_content.playlist_listbox.delete(0, tk.END)
            for pname in self.player.playlists.keys():
                self.main_content.playlist_listbox.insert(tk.END, pname)
            playlist_names = list(self.player.playlists.keys())
            try:
                index = playlist_names.index(self.player.current_playlist_name)
                self.main_content.playlist_listbox.select_set(index)
            except Exception:
                pass

    def play_song_by_index(self, index):
        self.player.current_index = index
        self.play_song()

    def play_song(self):
        song = self.player.play()
        if song:
            self.bottom_controls.current_offset = 0
            self.bottom_controls.now_playing_label.config(text=f"Now Playing: {os.path.basename(song)}")
            self.bottom_controls.progress_slider.config(to=int(self.player.song_length))
            self.bottom_controls.play_pause_btn.config(text="⏸")
        else:
            messagebox.showwarning("No Songs", "Please add songs to your library.")

    def toggle_play_pause(self):
        if not self.player.playing:
            self.play_song()
        elif self.player.paused:
            self.player.pause()
            self.bottom_controls.play_pause_btn.config(text="⏸")
        else:
            self.player.pause()
            self.bottom_controls.play_pause_btn.config(text="▶")

    def next_song(self):
        song = self.player.next_song()
        if song:
            self.bottom_controls.current_offset = 0
            self.bottom_controls.now_playing_label.config(text=f"Now Playing: {os.path.basename(song)}")
            self.bottom_controls.progress_slider.config(to=int(self.player.song_length))
            self.bottom_controls.play_pause_btn.config(text="⏸")

    def prev_song(self):
        song = self.player.prev_song()
        if song:
            self.bottom_controls.current_offset = 0
            self.bottom_controls.now_playing_label.config(text=f"Now Playing: {os.path.basename(song)}")
            self.bottom_controls.progress_slider.config(to=int(self.player.song_length))
            self.bottom_controls.play_pause_btn.config(text="⏸")

    def toggle_shuffle(self):
        self.player.toggle_shuffle()
        if self.player.shuffle:
            self.bottom_controls.shuffle_btn.config(text="Shuffle: On")
        else:
            self.bottom_controls.shuffle_btn.config(text="Shuffle: Off")

    def toggle_repeat(self):
        self.player.toggle_repeat()
        if self.player.repeat:
            self.bottom_controls.repeat_btn.config(text="Repeat: On")
        else:
            self.bottom_controls.repeat_btn.config(text="Repeat: Off")

    def skip_forward(self, event=None):
        elapsed = pygame.mixer.music.get_pos() / 1000.0
        current_time = self.bottom_controls.current_offset + elapsed
        new_time = current_time + 10
        if new_time > self.player.song_length:
            new_time = self.player.song_length - 1
        self.bottom_controls.seek_to(new_time)

    def skip_backward(self, event=None):
        elapsed = pygame.mixer.music.get_pos() / 1000.0
        current_time = self.bottom_controls.current_offset + elapsed
        new_time = current_time - 10
        if new_time < 0:
            new_time = 0
        self.bottom_controls.seek_to(new_time)

    def seek_to(self, pos):
        self.player.seek_to(pos)
        self.bottom_controls.current_offset = pos
        self.bottom_controls.progress_slider.set(pos)
        


