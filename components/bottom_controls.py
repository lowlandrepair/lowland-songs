import tkinter as tk
import pygame
from styles.theme import *

class BottomControls:
    def __init__(self, master, player, play_callbacks):
        self.master = master
        self.player = player
        self.play_callbacks = play_callbacks
        self.current_offset = 0

        # Main frame for bottom controls
        self.frame = tk.Frame(master, bg=BUTTON_COLOR, height=CONTROL_HEIGHT)
        self.frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.frame.grid_propagate(False)
        self.create_widgets()

    def create_widgets(self):
        # Left: Now Playing label
        self.now_playing_label = tk.Label(self.frame, text="Now Playing: None",
                                          fg="white", bg=BUTTON_COLOR, font=FONT)
        self.now_playing_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Center: Playback controls
        controls_frame = tk.Frame(self.frame, bg=BUTTON_COLOR)
        controls_frame.grid(row=0, column=1, padx=10, pady=5)
        self.prev_btn = tk.Button(controls_frame, text="⏮", font=("Helvetica", 20),
                                  fg="white", bg=BUTTON_COLOR, relief="flat",
                                  command=self.play_callbacks['prev'], activebackground=ACCENT_COLOR)
        self.prev_btn.grid(row=0, column=0, padx=5)
        self.play_pause_btn = tk.Button(controls_frame, text="▶", font=("Helvetica", 30),
                                        fg="white", bg=BUTTON_COLOR, relief="flat",
                                        command=self.play_callbacks['toggle'], activebackground=ACCENT_COLOR)
        self.play_pause_btn.grid(row=0, column=1, padx=5)
        self.next_btn = tk.Button(controls_frame, text="⏭", font=("Helvetica", 20),
                                  fg="white", bg=BUTTON_COLOR, relief="flat",
                                  command=self.play_callbacks['next'], activebackground=ACCENT_COLOR)
        self.next_btn.grid(row=0, column=2, padx=5)

        # Below playback controls: Timer labels and progress slider
        timer_frame = tk.Frame(self.frame, bg=BUTTON_COLOR)
        timer_frame.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.current_time_label = tk.Label(timer_frame, text="0:00", fg="white", bg=BUTTON_COLOR, font=SMALL_FONT)
        self.current_time_label.grid(row=0, column=0, sticky="w")
        self.progress_slider = tk.Scale(timer_frame, from_=0, to=100, orient="horizontal",
                                        bg=BUTTON_COLOR, fg="white", troughcolor=ACCENT_COLOR,
                                        length=300, showvalue=0, command=self.progress_slider_released)
        self.progress_slider.grid(row=0, column=1, padx=5)
        self.total_time_label = tk.Label(timer_frame, text="0:00", fg="white", bg=BUTTON_COLOR, font=SMALL_FONT)
        self.total_time_label.grid(row=0, column=2, sticky="e")

        # Right: Shuffle and Repeat buttons
        buttons_frame = tk.Frame(self.frame, bg=BUTTON_COLOR)
        buttons_frame.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.shuffle_btn = tk.Button(buttons_frame, text="Shuffle: Off", font=FONT,
                                     fg="white", bg=BUTTON_COLOR, relief="flat",
                                     command=self.play_callbacks['toggle_shuffle'], activebackground=ACCENT_COLOR)
        self.shuffle_btn.grid(row=0, column=0, padx=5)
        self.repeat_btn = tk.Button(buttons_frame, text="Repeat: Off", font=FONT,
                                    fg="white", bg=BUTTON_COLOR, relief="flat",
                                    command=self.play_callbacks['toggle_repeat'], activebackground=ACCENT_COLOR)
        self.repeat_btn.grid(row=0, column=1, padx=5)

        # Right: Volume slider
        volume_frame = tk.Frame(self.frame, bg=BUTTON_COLOR)
        volume_frame.grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.volume_slider = tk.Scale(volume_frame, from_=0, to=1, resolution=0.05,
                                      orient="horizontal", bg=BUTTON_COLOR, fg="white",
                                      troughcolor=ACCENT_COLOR, command=self.change_volume, length=80)
        self.volume_slider.set(0.5)
        self.volume_slider.grid(row=0, column=0, padx=5)

        self.update_progress()

    def change_volume(self, value):
        pygame.mixer.music.set_volume(float(value))

    def update_progress(self):
        if pygame.mixer.music.get_busy():
            elapsed = pygame.mixer.music.get_pos() / 1000.0
            current_time = self.current_offset + elapsed
            self.progress_slider.set(current_time)
            # Update timer labels
            self.current_time_label.config(text=self.format_time(current_time))
            self.total_time_label.config(text=self.format_time(self.player.song_length))
            if self.player.song_length and current_time >= self.player.song_length - 1:
                if self.player.repeat:
                    self.play_callbacks['toggle']()  # Restart song
                else:
                    self.play_callbacks['next']()
        self.master.after(200, self.update_progress)

    def progress_slider_released(self, value):
        pos = float(value)
        self.seek_to(pos)

    def seek_to(self, pos):
        was_paused = self.player.paused
        self.current_offset = pos
        pygame.mixer.music.stop()
        pygame.mixer.music.play(start=pos)
        if was_paused:
            pygame.mixer.music.pause()
        self.progress_slider.set(pos)

    def format_time(self, seconds):
        if seconds < 0:
            seconds = 0
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes}:{secs:02d}"
