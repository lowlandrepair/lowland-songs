import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from PIL import Image, ImageTk
import os
from styles.theme import *
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover  # Add this import
import requests
from io import BytesIO

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

        # Create context menu
        self.context_menu = tk.Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="Remove", command=self.remove_selected_song)

        self.selected_song_index = None

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
                                command=lambda idx=i: self.show_song_detail(idx))
                btn.grid(row=i // 3, column=i % 3, padx=10, pady=10, ipadx=10, ipady=10)
                btn.bind("<Button-3>", lambda e, idx=i: self.show_context_menu(e, idx))
        else:
            info = tk.Label(self.content_frame, text="No songs available. Add songs in Your Library.",
                            fg="white", bg=BG_COLOR, font=FONT)
            info.pack(pady=20)

    def show_context_menu(self, event, song_index):
        self.selected_song_index = song_index
        self.context_menu.post(event.x_root, event.y_root)

    def remove_selected_song(self):
        if self.selected_song_index is not None:
            removed_song = self.player.remove_song(self.selected_song_index)
            if removed_song:
                self.show_home()

    def show_song_detail(self, song_index):
        self.clear_content()
        song = self.player.playlists[self.player.current_playlist_name][song_index]
        song_name = os.path.basename(song)
        
        # Display song name
        song_label = tk.Label(self.content_frame, text=song_name, fg="white",
                              bg=BG_COLOR, font=HEADER_FONT)
        song_label.pack(pady=20)
        
        # Fetch and display cover photo and other metadata
        self.display_song_metadata(song)
        
        # Play button
        play_button = tk.Button(self.content_frame, text="Play", font=FONT,
                                command=lambda: self.play_song_callback(song_index), bg=BUTTON_COLOR, fg="white",
                                relief="flat", activebackground=ACCENT_COLOR)
        play_button.pack(pady=10)

    def seek(self, pos):
        self.player.seek_to(int(pos))

    def display_song_metadata(self, song_path):
        try:
            if song_path.endswith('.mp3'):
                audio = MP3(song_path, ID3=EasyID3)
                artist = audio.get('artist', ['Unknown Artist'])[0]
                album = audio.get('album', ['Unknown Album'])[0]
                title = audio.get('title', [os.path.basename(song_path)])[0]
            elif song_path.endswith('.mp4'):
                audio = MP4(song_path)
                artist = audio.tags.get('\xa9ART', ['Unknown Artist'])[0]
                album = audio.tags.get('\xa9alb', ['Unknown Album'])[0]
                title = audio.tags.get('\xa9nam', [os.path.basename(song_path)])[0]
            
            # Display artist and album
            artist_label = tk.Label(self.content_frame, text=f"Artist: {artist}", fg="white",
                                    bg=BG_COLOR, font=FONT)
            artist_label.pack(pady=5)
            album_label = tk.Label(self.content_frame, text=f"Album: {album}", fg="white",
                                   bg=BG_COLOR, font=FONT)
            album_label.pack(pady=5)
            
            # Fetch cover photo from iTunes API
            cover_photo = self.fetch_cover_photo(artist, album, title)
            if cover_photo:
                cover_image = Image.open(BytesIO(cover_photo))
                cover_image = cover_image.resize((300, 300), Image.ANTIALIAS)
                cover_photo = ImageTk.PhotoImage(cover_image)
                cover_label = tk.Label(self.content_frame, image=cover_photo, bg=BG_COLOR)
                cover_label.image = cover_photo  # Keep a reference to avoid garbage collection
                cover_label.pack(pady=20)
        except Exception as e:
            print(f"Error fetching metadata: {e}")

    def fetch_cover_photo(self, artist, album, title):
        try:
            query = f"{artist} {album} {title}".replace(" ", "+")
            url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"
            response = requests.get(url)
            data = response.json()
            if data['results']:
                cover_url = data['results'][0]['artworkUrl100'].replace("100x100", "600x600")
                cover_response = requests.get(cover_url)
                return cover_response.content
        except Exception as e:
            print(f"Error fetching cover photo: {e}")
        return None

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
                                            filetypes=(("MP3 Files", "*.mp3"), ("MP4 Files", "*.mp4"), ("WAV Files", "*.wav")))
        if songs:
            self.player.add_songs(songs)
            self.refresh_library()

    def library_double_click(self, event):
        selection = self.library_listbox.curselection()
        if selection:
            self.play_song_callback(selection[0])
