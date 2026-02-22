# Getting Started with Pobre Media Player

## Quick Start Guide

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed on your system.

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### Step 2: Install Dependencies

**Windows:**
```bash
# Using the install script
install.bat

# Or manually
pip install -r requirements.txt
```

**Linux:**
```bash
# Using the install script
chmod +x install.sh
./install.sh

# Or manually
pip3 install -r requirements.txt
```

### Step 3: Run the Player

**Windows:**
```bash
# Using the run script
run.bat

# Or manually
python player.py
```

**Linux:**
```bash
# Using the run script
chmod +x run.sh
./run.sh

# Or manually
python3 player.py
```

## How to Use

1. **Opening Videos:**
   - Drag and drop an MP4 file anywhere on the player window (on the dashed border placeholder or video area)
   - OR use `File > Open Video` menu
   - OR press `Ctrl+O`

2. **Player Interface:**
   - When no video is loaded, you'll see a dashed border with text "Drag and drop the video here to play"
   - Once a video is loaded, it will appear in the maximized video area (90% of window)
   - Controls are ultra-compact and take only 10% of the window height at the bottom

3. **Playback Controls:**
   - Click the Play/Pause button to control playback
   - Click anywhere on the progress bar to jump immediately to that position
   - Drag the progress slider to seek through the video
   - Use the volume slider to adjust volume
   - The time labels show current position and total duration (HH:MM:SS)

4. **Keyboard Shortcuts:**
   - `Space`: Play/Pause
   - `S`: Add current video time to Highlight CSV (if window is open)
   - `L`: Set last CSV row direction to Left
   - `R`: Set last CSV row direction to Right
   - `Left Arrow`: Rewind 3 seconds
   - `Right Arrow`: Forward 3 seconds
   - `Up Arrow`: Increase volume (+5%)
   - `Down Arrow`: Decrease volume (-5%)
   - `Ctrl+O`: Open video file
   - `Ctrl+Q`: Exit application

5. **Menu Options:**
   - **File > Open Video**: Browse for a video file
   - **File > Exit**: Close the application
   - **Tools > Highlight CSV**: Create timestamped markers and export to CSV
   - **Help > Check for Updates**: Check for new releases
   - **Help > About**: View application information

## Using Highlight CSV

The Highlight CSV tool allows you to create timestamped markers:

1. Click **Tools > Highlight CSV**
2. A new non-modal window opens (you can still interact with the video player)
3. While playing a video, press **'S' key** to automatically add the current timestamp
4. Press **'L' key** to set the last row direction to Left
5. Press **'R' key** to set the last row direction to Right
6. Or click **Add Row** to manually add entries
7. Fill in:
   - **Time**: Automatically filled when using 'S' key, or enter manually (HH:MM:SS format)
   - **Direction**: Select "Left" or "Right" from dropdown, or use L/R keys
8. Click **Play All** to automatically play the video at each recorded timestamp (3 seconds each)
9. Click **Save CSV** to export the data
10. Choose location and filename for your CSV file
11. The window can stay open while you continue watching and marking timestamps

## Building Portable Executable

### Windows:
```bash
# Run the build script
build.bat

# Or manually
pip install pyinstaller
pyinstaller --onefile --windowed --name=PobreMediaPlayer player.py
```

The executable will be in the `dist\` folder.

### Linux:
```bash
# Run the build script
chmod +x build.sh
./build.sh

# Or manually
pip install pyinstaller
pyinstaller --onefile --windowed --name=PobreMediaPlayer player.py
```

The executable will be in the `dist/` folder.

## Publishing to GitHub

1. **Initialize Git Repository:**
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Create GitHub Repository:**
   - Go to GitHub and create a new repository named "pobre-media-player"
   - Don't initialize with README (we already have one)

3. **Push to GitHub:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/pobre-media-player.git
git branch -M main
git push -u origin main
```

4. **Update Configuration:**
   - Open `player.py`
   - Change line 19: `GITHUB_REPO = "YOUR_USERNAME/pobre-media-player"`

5. **Create a Release:**
```bash
# Update VERSION in player.py first
git add player.py
git commit -m "Update version to 1.0.0"
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main
git push origin v1.0.0
```

6. **Automatic Builds:**
   - The GitHub Actions workflow will automatically build executables
   - Check the "Actions" tab on GitHub to see the progress
   - Once complete, a release will be created with Windows and Linux builds

## Customization

### Change Window Size:
In `player.py`, line 27:
```python
self.setGeometry(100, 100, 800, 600)  # x, y, width, height
```

### Add More Video Formats:
In `player.py`, line 99:
```python
"Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv);;..."
```

### Modify Default Window Title:
In `player.py`, line 26:
```python
self.setWindowTitle("Your Custom Title")
```

## Troubleshooting

### "No module named PyQt6"
```bash
pip install PyQt6
```

### "No module named requests"
```bash
pip install requests
```

### Video doesn't play
- Ensure the video codec is supported by your system
- Try a different video file
- Check if you have necessary media codecs installed

### Build fails on Linux
Install additional dependencies:
```bash
sudo apt-get install python3-dev
```

## Next Steps

- Test the application with different video formats
- Create your first release on GitHub
- Share with users!
- Check the README.md for advanced features and roadmap

---

Enjoy your new media player! 🎬
