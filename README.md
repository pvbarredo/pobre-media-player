# Pobre Media Player 🎬

A lightweight, portable media player built with Python and PyQt6 for Windows and Linux.

## Features ✨

- **MP4 Video Playback** - Play your favorite MP4 videos
- **Drag & Drop Support** - Simply drag and drop video files to play
- **Basic Controls** - Play, pause, and seek through videos
- **Cross-Platform** - Works on Windows and Linux
- **Auto-Update Checker** - Stay up to date with the latest releases
- **Portable** - No installation required

## Installation 🚀

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pobre-media-player.git
cd pobre-media-player
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage 💡

### Running the Player

```bash
python player.py
```

### Playing Videos

There are two ways to play videos:

1. **Drag and Drop**: Drag an MP4 file and drop it onto the player window
2. **File Menu**: Click `File > Open Video` and select your video file

### Controls

- **Play/Pause**: Click the play/pause button or press Space
- **Seek**: Click anywhere on the progress bar to jump to that position
- **Open File**: `Ctrl+O` or `File > Open Video`
- **Exit**: `Ctrl+Q` or `File > Exit`

## Menu Structure 📋

### File
- **Open Video** (Ctrl+O) - Select a video file to play
- **Exit** (Ctrl+Q) - Close the application

### Tools
- (Future features coming soon)

### Help
- **Check for Updates** - Check for new releases on GitHub
- **About** - View application information

## Building Portable Executable 📦

To create a standalone executable:

### Windows

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="PobreMediaPlayer" player.py
```

The executable will be in the `dist` folder.

### Linux

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="PobreMediaPlayer" player.py
```

## Supported Formats 🎥

Currently supported video formats:
- MP4
- AVI
- MKV
- MOV

## Configuration ⚙️

Before releasing, update the following in `player.py`:

```python
VERSION = "1.0.0"  # Update version number
GITHUB_REPO = "yourusername/pobre-media-player"  # Update with your GitHub username/repo
```

## Development 🛠️

### Project Structure

```
pobre-media-player/
├── player.py              # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── prompt/               # Project documentation
│   └── project_prompt.md # Project specifications
└── .gitignore           # Git ignore file
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Releasing 🎯

To create a new release:

1. Update the `VERSION` in `player.py`
2. Commit your changes
3. Create and push a tag:
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```
4. Create a release on GitHub with the tag
5. The "Check for Updates" feature will automatically detect new releases

## License 📄

MIT License - feel free to use this project for any purpose.

## Troubleshooting 🔧

### Video doesn't play
- Make sure the video file is a supported format (MP4, AVI, MKV, MOV)
- Check that you have the necessary codecs installed on your system
- Try converting the video to a different format

### Update check fails
- Verify your internet connection
- Check that the `GITHUB_REPO` variable is set correctly in `player.py`
- Ensure the repository is public or you have access

## Roadmap 🗺️

Future features planned:
- Volume control
- Fullscreen mode
- Playlist support
- Subtitle support
- Video filters and effects
- Remember last played position
- Recent files menu

## Support 💬

If you encounter any issues or have suggestions, please open an issue on GitHub.

---

Made with ❤️ using Python and PyQt6
