import sqlite3

def initialize_db():
    """Initialize the SQLite database and create the music table."""
    conn = sqlite3.connect('music_library.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS music (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            file_path TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def add_song(title, artist, file_path):
    """Add a new song to the database."""
    conn = sqlite3.connect('music_library.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO music (title, artist, file_path)
        VALUES (?, ?, ?)
    ''', (title, artist, file_path))
    conn.commit()
    conn.close()

def get_all_songs():
    """Retrieve all songs from the database."""
    conn = sqlite3.connect('music_library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, artist, file_path FROM music')
    songs = cursor.fetchall()
    conn.close()
    return songs
