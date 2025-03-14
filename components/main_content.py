import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import os
from styles.theme import *

class MainContent:
    def __init__(self, master, player, play_song_callback):
        self.master = master
        self.player = player
        self.play_song_callback = play_song_callback

        self.frame = tk.Frame(master, bg=BG_COLOR)
        self.frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.content_frame = tk.Frame(self.frame, bg=BG_COLOR)
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        self.current_view = None

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()
        self.current_view = "home"
        title = tk.Label(self.content_frame, text="Welcome to Lowland", fg="white",
                         bg=BG_COLOR, font=HEADER_FONT)
        title.pack(pady=20)
        playlist = self.player.playlists[self.player.current_playlist_name]
        if playlist:
            grid_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
            grid_frame.pack(pady=10)
            for i, song in enumerate(playlist):
                btn = tk.Button(grid_frame, text=os.path.basename(song), fg="white",
                                bg=BUTTON_COLOR, font=FONT, relief="flat",
                                command=lambda idx=i: self.play_song_callback(idx))
                btn.grid(row=i // 3, column=i % 3, padx=10, pady=10, ipadx=10, ipady=10)
        else:
            info = tk.Label(self.content_frame, text="No songs available. Add songs in Your Library.",
                            fg="white", bg=BG_COLOR, font=FONT)
            info.pack(pady=20)

    def show_search(self):
        self.clear_content()
        self.current_view = "search"
        search_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        search_frame.pack(fill="x", pady=10)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=FONT, width=30)
        search_entry.pack(side="left", padx=10)
        search_btn = tk.Button(search_frame, text="Search", font=FONT,
                               command=self.search_songs, bg=BUTTON_COLOR, fg="white",
                               relief="flat", activebackground=ACCENT_COLOR)
        search_btn.pack(side="left", padx=5)
        self.search_listbox = tk.Listbox(self.content_frame, font=FONT, bg=BUTTON_COLOR,
                                         fg="white", selectbackground=ACCENT_COLOR, relief="flat")
        self.search_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.search_listbox.bind("<Double-Button-1>", self.search_double_click)

    def search_songs(self):
        query = self.search_var.get().lower()
        self.search_listbox.delete(0, tk.END)
        self.search_results = []
        playlist = self.player.playlists[self.player.current_playlist_name]
        for i, song in enumerate(playlist):
            if query in os.path.basename(song).lower():
                self.search_listbox.insert(tk.END, os.path.basename(song))
                self.search_results.append(i)

    def search_double_click(self, event):
        selection = self.search_listbox.curselection()
        if selection:
            index = self.search_results[selection[0]]
            self.play_song_callback(index)

    def show_library(self, refresh_playlist_listbox_callback):
        self.clear_content()
        self.current_view = "library"
        playlist_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        playlist_frame.pack(side="left", fill="y", padx=10)
        self.playlist_listbox = tk.Listbox(playlist_frame, font=FONT, bg=BUTTON_COLOR,
                                           fg="white", selectbackground=ACCENT_COLOR,
                                           relief="flat", width=20)
        self.playlist_listbox.pack(fill="y", expand=True)
        self.playlist_listbox.bind("<<ListboxSelect>>", self.on_playlist_select)
        new_playlist_btn = tk.Button(playlist_frame, text="New Playlist", font=FONT,
                                     bg=BUTTON_COLOR, fg="white", relief="flat",
                                     command=self.create_new_playlist, activebackground=ACCENT_COLOR)
        new_playlist_btn.pack(pady=10)
        refresh_playlist_listbox_callback()

        song_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        song_frame.pack(side="left", fill="both", expand=True, padx=10)
        add_btn = tk.Button(song_frame, text="Add Songs", font=FONT,
                            bg=BUTTON_COLOR, fg="white", relief="flat",
                            command=self.add_songs, activebackground=ACCENT_COLOR)
        add_btn.pack(side="top", anchor="e", padx=10, pady=5)
        self.library_listbox = tk.Listbox(song_frame, font=FONT, bg=BUTTON_COLOR,
                                          fg="white", selectbackground=ACCENT_COLOR,
                                          relief="flat")
        self.library_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.library_listbox.bind("<Double-Button-1>", self.library_double_click)
        self.refresh_library()

    def on_playlist_select(self, event):
        selection = self.playlist_listbox.curselection()
        if selection:
            index = selection[0]
            playlist_names = list(self.player.playlists.keys())
            self.player.current_playlist_name = playlist_names[index]
            self.player.current_index = 0
            self.refresh_library()

    def create_new_playlist(self):
        new_name = simpledialog.askstring("New Playlist", "Enter playlist name:")
        if new_name:
            if new_name in self.player.playlists:
                messagebox.showerror("Error", "Playlist already exists!")
            else:
                self.player.playlists[new_name] = []
                self.player.current_playlist_name = new_name
                self.player.current_index = 0
                self.playlist_listbox.insert(tk.END, new_name)
                self.refresh_library()

    def refresh_library(self):
        if hasattr(self, 'library_listbox'):
            self.library_listbox.delete(0, tk.END)
            playlist = self.player.playlists[self.player.current_playlist_name]
            for song in playlist:
                self.library_listbox.insert(tk.END, os.path.basename(song))

    def add_songs(self):
        songs = filedialog.askopenfilenames(title="Select Songs",
                                            filetypes=(("MP3 Files", "*.mp3"), ("WAV Files", "*.wav")))
        if songs:
            self.player.add_songs(songs)
            self.refresh_library()

    def library_double_click(self, event):
        selection = self.library_listbox.curselection()
        if selection:
            self.play_song_callback(selection[0])
