# Pobre Media Player 🎬

A lightweight, portable media player built with Python and PyQt6 for Windows and Linux.

**Author:** Peter Barredo and his AI partner

## Features ✨

### Video Playback
- **MP4 Video Playback** - High-quality video playback with QMediaPlayer
- **Maximized Video Display** - Video occupies 90% of window height for optimal viewing
- **Drag & Drop Support** - Drag and drop video files anywhere in the application
- **Visual Placeholder** - Dashed border with clear "Drag and drop the video here to play" instructions

### Controls & UI
- **Ultra-Compact Controls** - Control bar takes only 10% of window height (72px max)
- **Intuitive Interface** - Play/pause button, seek slider, volume control, time display
- **Time Format** - HH:MM:SS format for precise time tracking
- **Window Icons** - Custom icons for main player and CSV tool windows
- **Footer** - Application branding in status bar

### Keyboard Shortcuts
- **Playback Controls** - Space for play/pause, arrows for seek/volume
- **Quick Timestamp Capture** - Press 'S' to instantly add current time to CSV
- **Direction Hot Keys** - Press 'L' or 'R' to set direction on last CSV row
- **Full Keyboard Navigation** - No mouse required for common operations

### Highlight CSV Tool
- **Timestamped Markers** - Record specific moments in videos with timestamps
- **Non-Modal Window** - CSV window stays accessible while controlling video
- **Structured Export** - Exports to CSV with Date, Placement, Camera, Time, Side columns
- **Quick Capture Workflow** - Press 'S' to add timestamp, 'L'/'R' to set direction
- **Play All Feature** - Sequentially play all recorded timestamps (3 seconds each)
- **Camera Default** - All entries default to "Cam1" camera

### Developer Features
- **Cross-Platform** - Works on Windows and Linux
- **Auto-Update Checker** - Checks GitHub releases for new versions
- **GitHub Actions CI/CD** - Automated builds and releases on git tag push
- **Portable Executables** - Single-file .exe (Windows) and binary (Linux)
- **No Installation Required** - Run directly from executable

## Installation 🚀

### For End Users

Download the latest release from the [Releases page](https://github.com/pvbarredo/pobre-media-player/releases):

#### Windows Installation

1. Download `PobreMediaPlayer.exe`
2. Double-click to run (you may see a SmartScreen warning - see below)

#### Linux Installation

1. Download `PobreMediaPlayer`
2. Open terminal in the download folder
3. Make it executable (if needed - newer releases have this pre-set):
   ```bash
   chmod +x PobreMediaPlayer
   ```
4. Run it:
   ```bash
   ./PobreMediaPlayer
   ```

**Alternative (using file manager):**
- Right-click file → Properties → Permissions tab
- Check "Allow executing file as program" (may already be checked on newer releases)
- Double-click the file to run

**System Requirements:** Ubuntu 20.04+, Debian 11+, Fedora 33+ or equivalent (GLIBC 2.31+)

No installation required - just download and run!

#### Windows Security Warning ⚠️

When running the Windows executable for the first time, you may see a **Windows SmartScreen warning** saying "Windows protected your PC" or that the app might be dangerous.

**This is normal and safe.** The warning appears because:
- The executable is not digitally signed with a code signing certificate
- Windows doesn't recognize the publisher (signing certificates cost $100-$400/year)
- This is common for open-source projects and indie software

**To run the application:**

1. Click **"More info"** on the SmartScreen warning dialog
2. Click the **"Run anyway"** button that appears
3. The app will launch normally

**Alternative method:** Right-click the `.exe` file → Properties → Check "Unblock" → Apply → OK, then run the file.

**The app is safe** - it's open source, and you can verify the code yourself in this repository. The executable is built automatically by GitHub Actions from the source code.

### For Developers

#### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

#### Setup

1. Clone the repository:
```bash
git clone https://github.com/pvbarredo/pobre-media-player.git
cd pobre-media-player
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python player.py
```

## Usage 💡

### Running the Player

#### From Source
```bash
python player.py
```

#### From Executable
- **Windows**: Double-click `PobreMediaPlayer.exe`
- **Linux**: Run `./PobreMediaPlayer`

### Playing Videos

There are two ways to load videos:

1. **Drag and Drop**: Drag an MP4 file and drop it anywhere on the player window (placeholder or video area)
2. **File Menu**: Click `File > Open Video` (Ctrl+O) and select your video file

### Basic Controls

- **Play/Pause**: Click the play button or press `Space`
- **Seek**: Drag the progress slider or click anywhere on it to jump to that position
- **Volume**: Drag the volume slider or use `Up Arrow` / `Down Arrow` keys
- **Skip Forward**: Press `Right Arrow` to skip forward 3 seconds
- **Skip Backward**: Press `Left Arrow` to skip backward 3 seconds

### Highlight CSV Tool 📝

The Highlight CSV tool allows you to create timestamped markers while watching videos - perfect for sports analysis, video editing, or any task requiring precise timestamp tracking.

#### Opening the Tool
- Click `Tools > Highlight CSV` in the menu bar

#### Adding Timestamps
1. **Play your video** to the moment you want to mark
2. **Press 'S' key** - the current video time is instantly added to the CSV table
3. **Press 'L' or 'R' key** - sets the last row's direction to Left or Right
4. Repeat as needed while video continues playing

#### CSV Table Columns
- **Time**: Video timestamp in HH:MM:SS format
- **Direction**: Left or Right (dropdown selection)

#### Exporting CSV
Click the "Save CSV" button to export timestamps. The exported CSV includes:
- **Date**: Current date (format: M/D/YYYY)
- **Placement**: Row number (1, 2, 3, ...)
- **Camera**: Always "Cam1" (default camera setting)
- **Time**: Video timestamp (HH:MM:SS)
- **Side**: Direction in lowercase (left/right)

Example CSV output:
```
Date,2/23/2026,,,
Placement,Camera,Time,Side
1,Cam1,00:01:23,left
2,Cam1,00:02:15,right
3,Cam1,00:03:47,left
```

#### Play All Feature
Click "Play All" to automatically:
1. Navigate to each timestamp in the table sequentially
2. Play 3 seconds of video at each timestamp
3. Move to the next timestamp automatically

This is useful for reviewing all marked moments quickly.

#### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Play/Pause |
| `S` | Add current video time to Highlight CSV |
| `L` | Set last CSV row direction to Left |
| `R` | Set last CSV row direction to Right |
| `Left Arrow` | Rewind 3 seconds |
| `Right Arrow` | Forward 3 seconds |
| `Up Arrow` | Increase volume (+5%) |
| `Down Arrow` | Decrease volume (-5%) |
| `Ctrl+O` | Open video file |
| `Ctrl+Q` | Exit application |

## Menu Structure 📋

### File
- **Open Video** (Ctrl+O) - Select and load a video file
- **Exit** (Ctrl+Q) - Close the application

### Tools
- **Highlight CSV** - Open the timestamp tracking tool (non-modal window)

### Help
- **Check for Updates** - Query GitHub API for latest release version
- **About** - Display application info, version, author, and keyboard shortcuts

## Building Executables 📦

### Automated Build (Recommended)

The project includes GitHub Actions workflow that automatically builds executables for both Windows and Linux when you push a git tag:

1. Update `VERSION` in `player.py`
2. Commit your changes
3. Create and push a tag:
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

GitHub Actions will:
- Build Windows executable (`PobreMediaPlayer.exe`)
- Build Linux executable (`PobreMediaPlayer`)
- Create a GitHub release with both executables attached
- Users can download and run immediately

### Manual Build

To build locally using PyInstaller:

#### Windows

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="PobreMediaPlayer" player.py
```

The executable will be in the `dist/` folder.

#### Linux

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="PobreMediaPlayer" player.py
```

The executable will be in the `dist/` folder.

## Supported Formats 🎥

The application uses PyQt6's QMediaPlayer, which supports various formats depending on the system's multimedia backend:

### Commonly Supported
- **MP4** (H.264/AAC) - Primary tested format
- **AVI** - Widely supported
- **MKV** - Matroska container
- **MOV** - QuickTime format
- **WebM** - Web video format

### Platform-Specific Notes
- **Windows**: Uses Windows Media Foundation
- **Linux**: Uses GStreamer (may require `gstreamer` packages)

If a video doesn't play, try converting to MP4 with H.264 video and AAC audio codecs.

## Technical Details 🔧

### Architecture

- **GUI Framework**: PyQt6 (Qt 6.x bindings for Python)
  - Cross-platform native widgets
  - Hardware-accelerated video rendering
  - Modern Qt 6 API
  
- **Media Backend**: PyQt6.QtMultimedia
  - QMediaPlayer for playback control
  - QAudioOutput for audio management
  - QVideoWidget for display
  - Platform-native decoders (Media Foundation on Windows, GStreamer on Linux)

- **Networking**: requests library
  - GitHub Releases API integration
  - Update checking mechanism

### UI Layout

```
QMainWindow (1280x720)
├── Menu Bar
│   ├── File (Open Video, Exit)
│   ├── Tools (Highlight CSV)
│   └── Help (Check for Updates, About)
├── Central Widget (QVBoxLayout, no margins/spacing)
│   ├── QStackedWidget (90% height, expanding)
│   │   ├── [0] Placeholder (QLabel with dashed border CSS)
│   │   └── [1] QVideoWidget (media player output)
│   └── Controls Container (QHBoxLayout, max 72px height)
│       ├── Play/Pause Button (NoFocus policy)
│       ├── Position Slider (NoFocus policy)
│       ├── Time Labels (current/total in HH:MM:SS)
│       └── Volume Slider (NoFocus policy, 0-100 range)
└── Status Bar
    └── Footer Label ("Pedro Barredo @ 2026", right-aligned, permanent)
```

### Event Handling

- **Drag-Drop**: Enabled on QMainWindow, QVideoWidget, and placeholder
  - Accepts file:/// URLs
  - Filters for video/* mime types
  - Event filter on placeholder for nested drag-drop
  
- **Keyboard**: 
  - `keyPressEvent()` override in VideoPlayer
  - Play button and sliders set to NoFocus to prevent event hijacking
  - Modifiers processed for Ctrl+O, Ctrl+Q
  
- **CSV Window**:
  - Non-modal (shows independently, doesn't block main window)
  - Parent reference for accessing media player state
  - QTimer-based sequential playback

### Build Process

PyInstaller creates single-file executables:
```bash
pyinstaller --onefile --windowed --name="PobreMediaPlayer" player.py
```

Flags:
- `--onefile`: Bundle everything into single executable
- `--windowed`: No console window (GUI app)
- `--name`: Output executable name

## Development 🛠️

### Project Structure

```
pobre-media-player/
├── .github/
│   └── workflows/
│       └── release.yml        # GitHub Actions CI/CD for automated builds
├── prompt/
│   └── project_prompt.md     # Complete project specifications and features
├── player.py                 # Main application (VideoPlayer and HighlightCSVWindow classes)
├── requirements.txt          # Python dependencies (PyQt6, requests)
├── README.md                # This file
├── GETTING_STARTED.md       # Quick start guide for users
└── .gitignore              # Git ignore patterns
```

### Key Components

#### player.py
- **VideoPlayer** (QMainWindow): Main window with video playback
  - QMediaPlayer for video playback with QAudioOutput
  - QStackedWidget: Switches between placeholder (index 0) and video widget (index 1)
  - Drag-drop event handling on all widgets
  - Keyboard event handling (Space, S, L, R, Arrow keys)
  - Menu bar with File, Tools, Help menus
  - Status bar with footer label
  
- **HighlightCSVWindow** (QMainWindow): Non-modal CSV timestamp tool
  - QTableWidget with Time and Direction columns
  - Add rows manually or via parent player
  - Save to CSV with custom format (Date header, Placement/Camera/Time/Side columns)
  - Play All feature with QTimer for sequential playback

#### .github/workflows/release.yml
- Triggers on git tag push (v*.*.*)
- Builds Windows executable using PyInstaller on windows-latest runner
- Builds Linux executable using PyInstaller on ubuntu-20.04 runner (for GLIBC 2.31 compatibility)
- Sets execute permissions on Linux binary with `chmod +x`
- Uploads artifacts using actions/upload-artifact@v4
- Creates GitHub release with both executables using softprops/action-gh-release@v2
- Requires `permissions: contents: write` for release creation

### Configuration

Before releasing, update these constants in `player.py`:

```python
VERSION = "1.0.0"  # Update version number for releases
```

### Dependencies

```
PyQt6>=6.6.0         # GUI framework and multimedia
requests>=2.31.0     # HTTP library for GitHub API calls
```

### Development Workflow

1. **Make changes** to `player.py` or other files
2. **Test locally** by running `python player.py`
3. **Update VERSION** in `player.py` if releasing
4. **Commit changes**: `git commit -am "Description of changes"`
5. **Create tag**: `git tag -a v1.0.0 -m "Release message"`
6. **Push tag**: `git push origin v1.0.0`
7. **GitHub Actions builds** executables automatically
8. **Release created** with executables attached

### Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly on your platform
5. Commit your changes (`git commit -am 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please ensure your code:
- Follows existing code style
- Works on both Windows and Linux (if possible to test)
- Doesn't break existing keyboard shortcuts or features
- Updates README.md if adding new features

## Releasing 🎯

### Automated Release Process

The project uses GitHub Actions for automated builds and releases:

1. **Update VERSION** in `player.py`:
   ```python
   VERSION = "1.0.1"  # Increment version number
   ```

2. **Commit your changes**:
   ```bash
   git add player.py
   git commit -m "Bump version to 1.0.1"
   ```

3. **Create an annotated tag**:
   ```bash
   git tag -a v1.0.1 -m "Release version 1.0.1 - Added new features"
   ```

4. **Push tag to GitHub**:
   ```bash
   git push origin v1.0.1
   ```

5. **GitHub Actions automatically**:
   - Checks out code on Windows and Linux runners
   - Installs Python dependencies
   - Builds executables with PyInstaller (`--onefile --windowed`)
   - Creates GitHub release
   - Uploads Windows and Linux executables as release assets

6. **Users can now**:
   - Visit the Releases page
   - Download platform-specific executable
   - Use "Check for Updates" in the app to see the new version

### Release Workflow Details

The `.github/workflows/release.yml` workflow:
- **Trigger**: Push of tags matching `v*.*.*` pattern
- **Build Jobs**: Run in parallel on `windows-latest` and `ubuntu-20.04` (older Ubuntu for better Linux compatibility)
- **Artifacts**: Uploaded with retention period
- **Release**: Created with `permissions: contents: write`
- **Asset Names**: `PobreMediaPlayer.exe` (Windows), `PobreMediaPlayer` (Linux)

### Manual Release (Alternative)

If you prefer manual releases:

1. Build executables locally (see "Building Executables" section)
2. Create a release on GitHub web interface
3. Upload `dist/PobreMediaPlayer.exe` and `dist/PobreMediaPlayer` as assets
4. Tag the release with version (e.g., v1.0.1)

## Troubleshooting 🔧

### Video Issues

**Problem**: Video doesn't play or shows black screen
- **Solution**: Check that the video format is supported by your system's media backend
- **Windows**: Ensure Windows Media Foundation is enabled
- **Linux**: Install GStreamer: `sudo apt install gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad`
- **All platforms**: Try converting video to MP4 (H.264/AAC)

**Problem**: Audio but no video, or video but no audio
- **Solution**: Codec issue - convert to MP4 with standard codecs
- **Alternative**: Install codec packs on your system

### Windows Security Warning

**Problem**: Windows shows "Windows protected your PC" or SmartScreen warning when running the .exe file
- **Solution**: This is normal for unsigned executables. Click "More info" then "Run anyway"
- **Alternative**: Right-click .exe → Properties → Check "Unblock" → Apply → OK
- **Why it happens**: The app isn't digitally signed (code signing certificates are expensive)
- **Is it safe?**: Yes - the app is open source, built by GitHub Actions from verified code

### Linux Execution Issues

**Problem**: "Could Not Display" or "No application installed for executable files" error when double-clicking
- **Cause**: File doesn't have execute permissions set (fixed in newer releases, but may occur with older downloads)
- **Solution**: Run `chmod +x PobreMediaPlayer` in terminal, then run `./PobreMediaPlayer`
- **Alternative**: Right-click file → Properties → Permissions → Check "Allow executing file as program"
- **Note**: Releases from v1.0.1+ have execute permissions pre-set

**Problem**: `GLIBC_2.XX not found` error when running the executable
- **Cause**: Your Linux distribution has an older version of GLIBC than required
- **Solution**: Download a newer version (releases are built on Ubuntu 20.04 for compatibility with most distros)
- **Workaround**: Run from source instead:
  ```bash
  git clone https://github.com/pvbarredo/pobre-media-player.git
  cd pobre-media-player
  pip install -r requirements.txt
  python player.py
  ```
- **Supported distros**: Ubuntu 20.04+, Debian 11+, Fedora 33+, or equivalent

**Problem**: Application won't start or crashes immediately on Linux
- **Solution**: Install required system packages:
  ```bash
  sudo apt install libxcb-xinerama0 libxcb-cursor0  # Qt dependencies
  sudo apt install gstreamer1.0-plugins-base gstreamer1.0-plugins-good  # Video playback
  ```
- **For other distros**: Install equivalent Qt6 and GStreamer packages

### Keyboard Shortcut Issues

**Problem**: Arrow keys or Space key not working
- **Solution**: Click on the video area or window background (not on buttons/sliders)
- **Technical**: Buttons with focus hijack keyboard events; all interactive widgets set to NoFocus policy

**Problem**: 'S', 'L', 'R' keys not adding to CSV or updating direction
- **Solution**: Ensure Highlight CSV window is open (Tools > Highlight CSV)
- **Technical**: Keys only work when `highlight_csv_window` reference exists and window is visible

### CSV Export Issues

**Problem**: CSV file is empty or malformed
- **Solution**: Ensure you added rows to the table before saving
- **Technical**: Check that table has items with `QTableWidgetItem` in column 0 and `QComboBox` widget in column 1

**Problem**: Date format showing leading zeros
- **Solution**: This is platform-specific; Windows uses `%#m/%#d/%Y`, Unix uses `%-m/%-d/%Y`
- **Both formats**: Remove leading zeros automatically

### Update Checker Issues

**Problem**: "Check for Updates" shows error or times out
- **Solutions**:
  - Verify internet connection
  - Check that `GITHUB_REPO` constant is correct in `player.py`
  - Ensure repository is public
  - GitHub API rate limits: 60 requests/hour for unauthenticated requests
- **Technical**: Uses `requests.get(f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest")`

### Build Issues

**Problem**: PyInstaller build fails with import errors
- **Solution**: Ensure all dependencies installed: `pip install -r requirements.txt`
- **Solution**: Update PyInstaller: `pip install --upgrade pyinstaller`

**Problem**: Built executable is very large
- **Solution**: This is normal; PyInstaller bundles Python interpreter and all dependencies
- **Typical sizes**: 80-150 MB depending on platform

**Problem**: Executable works on build machine but not on others
- **Windows**: Distribute with Microsoft Visual C++ Redistributable
- **Linux**: Build on older distro for better compatibility, or provide AppImage

### GitHub Actions Issues

**Problem**: Release creation fails with 403 error
- **Solution**: Ensure workflow has `permissions: contents: write` in YAML
- **Solution**: Check repository settings allow actions to create releases

**Problem**: Builds fail on one platform but not the other
- **Solution**: Check platform-specific code (e.g., date formatting with `os.name`)
- **Solution**: Review workflow logs for specific error messages

### Development Issues

**Problem**: Changes to UI not appearing
- **Solution**: Restart the application (some Qt changes require restart)
- **Solution**: Clear any cached `.pyc` files: `find . -type f -name "*.pyc" -delete`

**Problem**: Drag-drop not working on specific widget
- **Solution**: Call `setAcceptDrops(True)` on widget
- **Solution**: Install event filter if widget is nested: `widget.installEventFilter(self)`

## Known Limitations ⚠️

- **Single Video**: Only one video can be loaded at a time (no playlist)
- **CSV Camera Field**: Always defaults to "Cam1" (hardcoded)
- **CSV Columns**: Table only shows Time and Direction; Placement, Camera, Date added on export
- **Video Formats**: Limited to what system multimedia backend supports
- **Update Check**: Manual only (no auto-check on startup)
- **Window Size**: Fixed 1280x720 on startup (user can resize, but layout optimized for this)

## Roadmap 🗺️

### Planned Features
- [ ] Fullscreen mode toggle
- [ ] Playlist support (multiple videos)
- [ ] Subtitle support (.srt files)
- [ ] Recent files menu
- [ ] Mute button
- [ ] Playback speed control (0.5x - 2.0x)
- [ ] Remember last window size/position
- [ ] Dark theme option
- [ ] CSV camera name customization
- [ ] Frame-by-frame stepping
- [ ] Screenshot capture
- [ ] Loop selected section

### Potential Improvements
- [ ] Auto-check for updates on startup (with user permission)
- [ ] Export highlights as video clips
- [ ] Multiple camera support in CSV
- [ ] Customizable keyboard shortcuts
- [ ] Session recovery (remember last played video and position)
- [ ] Video filters (brightness, contrast, etc.)

## Performance Notes 📊

### Resource Usage
- **Memory**: ~80-120 MB baseline + video buffer
- **CPU**: Minimal when paused; codec-dependent when playing
- **Startup Time**: 1-3 seconds (executable), <1 second (Python)

### Best Practices
- For large videos (>2GB), use efficient codecs (H.264)
- CSV with >1000 rows may slow table rendering
- Play All feature loads positions sequentially (minimal memory impact)

## Testing 🧪

### Manual Testing Checklist

- [ ] Drag-drop MP4 onto window (placeholder and video area)
- [ ] File > Open Video loads and plays video
- [ ] Space bar toggles play/pause
- [ ] Arrow keys: Left/Right seek ±3s, Up/Down volume ±5%
- [ ] Progress slider: Click jumps to position, drag seeks smoothly
- [ ] Volume slider: Adjust from 0-100%
- [ ] Tools > Highlight CSV opens non-modal window
- [ ] Press 'S' adds current timestamp to CSV table
- [ ] Press 'L'/'R' updates last row direction
- [ ] Play All in CSV window sequences through timestamps
- [ ] Save CSV creates file with correct format (Date, Placement, Camera, Time, Side)
- [ ] Help > Check for Updates queries GitHub API
- [ ] Help > About shows version, author, keyboard shortcuts
- [ ] Footer shows "Pedro Barredo @ 2026"
- [ ] Window icons display on taskbar/window title

### Platform-Specific Testing
- **Windows**: Test on Windows 10/11, verify .exe runs without Python installed
- **Linux**: Test on Ubuntu/Debian, verify binary runs with execute permission

## License 📄

MIT License - free to use for any purpose.

Copyright (c) 2026 Peter Barredo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

## Support 💬

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/pvbarredo/pobre-media-player/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pvbarredo/pobre-media-player/discussions)
- **Documentation**: This README and `prompt/project_prompt.md`

### Reporting Bugs

When reporting bugs, please include:
1. Operating system and version
2. Python version (if running from source)
3. Steps to reproduce the issue
4. Expected vs actual behavior
5. Screenshots if applicable
6. Error messages from terminal/console

### Feature Requests

Feature requests are welcome! Please:
1. Check existing issues/discussions first
2. Describe the use case and benefit
3. Suggest how it might work
4. Consider contributing code if you can

---

**Made with ❤️ using Python and PyQt6**

**Author:** Peter Barredo and his AI partner  
**Repository:** [github.com/pvbarredo/pobre-media-player](https://github.com/pvbarredo/pobre-media-player)
