# Lowland Music Player

A modern desktop music player application built with Python, Tkinter, and Pygame.

## Features
- Play/Pause/Stop controls
- Shuffle and Repeat modes
- Playlist management
- Seek functionality
- Modern UI with custom theme support
- Keyboard shortcuts for playback control

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required libraries:
```bash
pip install pygame mutagen
```

3. Clone this repository:
```bash
git clone https://github.com/yourusername/lowland-music-player.git
```

4. Navigate to the project directory:
```bash
cd lowland-music-player
```

## Usage

Run the application:
```bash
python main.py
```

### Controls
- Space: Play/Pause
- Right Arrow: Skip forward 10 seconds
- Left Arrow: Skip backward 10 seconds
- Click and drag the progress bar to seek
- Use the sidebar to navigate between Home, Search, and Library views

## Project Structure
```
.
├── main.py                # Main application entry point
├── player.py              # Music player logic and controls
├── ui.py                  # Main UI implementation
├── components/            # UI components
│   ├── sidebar.py         # Navigation sidebar
│   ├── main_content.py    # Main content area
│   └── bottom_controls.py # Playback controls
└── styles/                # UI theme and styling
    └── theme.py           # Color scheme and styles
```

## Requirements
- Python 3.7+
- Pygame (for audio playback)
- Mutagen (for MP3 metadata)


