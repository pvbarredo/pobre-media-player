# Pobre Media Player - Project Specification

## Project Overview

A lightweight, portable cross-platform media player built with Python and PyQt6, designed for video playback with advanced timestamp tracking capabilities.

**Author:** Peter Barredo and his AI partner  
**Version:** 1.0.0  
**Repository:** https://github.com/pvbarredo/pobre-media-player

## Purpose

Provide a simple yet powerful video player with emphasis on:
- Portability (single executable, no installation)
- Timestamp tracking for video analysis (sports, editing, etc.)
- Keyboard-driven workflow for efficiency
- Cross-platform compatibility (Windows & Linux)
- Automated build/release pipeline

## Key Features

### Video Playback
- MP4 and other common formats (AVI, MKV, MOV, WebM)
- High-quality playback using platform-native decoders
- Maximized video display (90% of window height)
- Visual placeholder with dashed border when no video loaded
- Drag-drop support anywhere in application window

### User Interface
- Window size: 1280x720 pixels (resizable)
- Ultra-compact control bar (10% height, 72px max)
- Time display in HH:MM:SS format
- Window icons for main player and CSV tool
- Status bar footer: "Pedro Barredo @ 2026"
- Clean, minimal design focused on video content

### Playback Controls
- Play/pause button with standard icons
- Seek slider with click-to-jump functionality
- Volume slider (0-100%, default 70%)
- Time labels showing current/total time
- All interactive controls set to NoFocus policy (preserves keyboard shortcuts)

### Keyboard Shortcuts
- **Space**: Toggle play/pause
- **S**: Add current video timestamp to Highlight CSV
- **L**: Set last CSV row direction to "Left"
- **R**: Set last CSV row direction to "Right"
- **Left Arrow**: Rewind 3 seconds
- **Right Arrow**: Forward 3 seconds
- **Up Arrow**: Increase volume by 5%
- **Down Arrow**: Decrease volume by 5%
- **Ctrl+O**: Open video file dialog
- **Ctrl+Q**: Exit application

### Highlight CSV Tool
- **Purpose**: Track specific moments in videos with timestamps and directional markers
- **Window Type**: Non-modal (doesn't block main player interaction)
- **Table Columns** (display):
  - Time: HH:MM:SS format
  - Direction: Dropdown (Left/Right options)
- **CSV Export Format**:
  ```
  Date,M/D/YYYY,,,
  Placement,Camera,Time,Side
  1,Cam1,00:01:23,left
  2,Cam1,00:02:15,right
  ```
- **Features**:
  - Add rows manually with "Add Row" button
  - Quick capture: Press 'S' key in main window to add current video time
  - Quick direction: Press 'L' or 'R' to set last row's direction
  - Play All: Sequentially play 3 seconds at each timestamp
  - Save CSV: Export with date header, numbered placements, default camera "Cam1"

### Update Mechanism
- Queries GitHub Releases API for latest version
- Manual check via Help > Check for Updates
- Compares semantic versions (current vs latest)
- Shows message with update availability and download link
- No automatic updates (user downloads manually)

## Technical Stack

### Core Technologies
- **Python**: 3.8+ (language)
- **PyQt6**: 6.6.0+ (GUI framework)
  - QtWidgets: UI components
  - QtMultimedia: Media playback (QMediaPlayer, QAudioOutput)
  - QtMultimediaWidgets: Video display (QVideoWidget)
  - QtCore: Event system, timers, signals
  - QtGui: Events, actions, styling
- **requests**: 2.31.0+ (HTTP library for GitHub API)
- **csv**: Standard library (CSV export)
- **datetime**: Standard library (timestamps and date formatting)
- **os**: Standard library (platform detection for date format)

### Build Tools
- **PyInstaller**: Creates standalone executables
- **GitHub Actions**: CI/CD for automated builds and releases

## Architecture

### Main Classes

#### VideoPlayer (QMainWindow)
Main application window containing video player and all controls.

**Key Components:**
- `media_player`: QMediaPlayer instance for video playback
- `audio_output`: QAudioOutput instance for audio management
- `video_widget`: QVideoWidget for rendering video
- `placeholder_widget`: QLabel with dashed border and instructions
- `stacked_widget`: QStackedWidget switching between placeholder (index 0) and video (index 1)
- `highlight_csv_window`: Reference to HighlightCSVWindow instance (created on demand)

**Key Methods:**
- `__init__()`: Initialize media player, widgets, UI
- `init_ui()`: Build UI layout (stacked widget, controls, footer)
- `create_menu_bar()`: Create File/Tools/Help menus
- `load_video(file_path)`: Load video file and switch to video widget
- `toggle_play_pause()`: Play/pause with button icon updates
- `position_changed(position)`: Update slider and time label during playback
- `duration_changed(duration)`: Set slider range and total time label
- `keyPressEvent(event)`: Handle keyboard shortcuts
- `dragEnterEvent()`, `dropEvent()`: Handle drag-drop file loading
- `eventFilter()`: Handle drag-drop on nested placeholder widget
- `open_highlight_csv()`: Create/show CSV window
- `format_time(ms)`: Convert milliseconds to HH:MM:SS string
- `check_for_updates()`: Query GitHub API for latest release
- `show_about()`: Display About dialog

#### HighlightCSVWindow (QMainWindow)
Non-modal window for timestamp tracking and CSV export.

**Key Components:**
- `player`: Reference to parent VideoPlayer for accessing media player state
- `table`: QTableWidget with Time and Direction columns
- `current_playing_index`: Track position during Play All sequence
- `play_timer`: QTimer for 3-second intervals during Play All

**Key Methods:**
- `__init__(parent)`: Initialize table, buttons, layout
- `add_row()`: Add empty row with current time and default direction
- `add_row_with_time(time_value)`: Add row with specific timestamp (called by 'S' key)
- `update_last_direction(direction)`: Set last row dropdown to Left/Right (called by 'L'/'R' keys)
- `save_csv()`: Export to CSV with Date header and Placement/Camera/Time/Side format
- `play_all_timestamps()`: Start sequential playback of all timestamps
- `check_play_next()`: Timer callback to advance to next timestamp
- `parse_time_to_ms(time_str)`: Convert HH:MM:SS to milliseconds for seeking

### UI Layout Hierarchy

```
VideoPlayer (QMainWindow)
├── Menu Bar
│   ├── File Menu
│   │   ├── Open Video (Ctrl+O)
│   │   └── Exit (Ctrl+Q)
│   ├── Tools Menu
│   │   └── Highlight CSV
│   └── Help Menu
│       ├── Check for Updates
│       └── About
├── Central Widget (QWidget)
│   └── Main Layout (QVBoxLayout, no margins, no spacing)
│       ├── Stacked Widget (QStackedWidget, expanding, 90% height)
│       │   ├── [Index 0] Placeholder (QLabel)
│       │   │   └── Text: "Drag and drop the video here to play"
│       │   │       Style: Dashed border, centered text, gray background
│       │   └── [Index 1] Video Widget (QVideoWidget)
│       │       └── Connected to media_player video output
│       └── Controls Container (QWidget, max height 72px, 10% of window)
│           └── Controls Layout (QHBoxLayout)
│               ├── Play Button (QPushButton, NoFocus)
│               │   └── Icons: SP_MediaPlay / SP_MediaPause
│               ├── Position Slider (QSlider, horizontal, NoFocus)
│               ├── Current Time Label (QLabel, "00:00:00")
│               ├── "/" Label (QLabel)
│               ├── Total Time Label (QLabel, "00:00:00")
│               ├── "Volume:" Label (QLabel)
│               └── Volume Slider (QSlider, horizontal, NoFocus, 0-100)
└── Status Bar
    └── Footer Label (QLabel, "Pedro Barredo @ 2026", right-aligned, permanent widget)
```

```
HighlightCSVWindow (QMainWindow)
├── Central Widget (QWidget)
│   └── Layout (QVBoxLayout)
│       ├── Table (QTableWidget, 2 columns)
│       │   ├── Column 0: "Time" (QTableWidgetItem, read-only)
│       │   └── Column 1: "Direction" (QComboBox with Left/Right)
│       └── Button Layout (QHBoxLayout)
│           ├── Save CSV Button (QPushButton)
│           ├── Play All Button (QPushButton)
│           └── Add Row Button (QPushButton)
└── Status Bar (shows feedback messages)
```

## Event Flow

### Video Loading via Drag-Drop
1. User drags video file over window
2. `dragEnterEvent()` checks for URLs, accepts if contains video file
3. User drops file
4. `dropEvent()` extracts file path, calls `load_video()`
5. `load_video()` sets media source, switches stacked widget to index 1 (video), starts playback

### Timestamp Capture with 'S' Key
1. User presses 'S' while video playing
2. `keyPressEvent()` in VideoPlayer detects key
3. Checks if `highlight_csv_window` exists and is visible
4. Gets current position from `media_player.position()` (milliseconds)
5. Converts to HH:MM:SS using `format_time()`
6. Calls `highlight_csv_window.add_row_with_time(time_str)`
7. CSV window adds row to table with time and default "Left" direction
8. Table auto-scrolls to new row

### Play All Timestamps
1. User clicks "Play All" button in CSV window
2. `play_all_timestamps()` checks table has rows
3. Pauses main player, sets `current_playing_index` to 0
4. Reads first timestamp, converts to milliseconds, seeks player
5. Starts playback
6. Starts `play_timer` with 3000ms (3 seconds) timeout
7. When timer fires, `check_play_next()` increments index
8. If more rows exist, repeats steps 4-7
9. When all rows played, pauses player, stops timer

### CSV Export
1. User clicks "Save CSV" button
2. `save_csv()` opens file dialog with default filename `highlights_YYYYMMDD_HHMMSS.csv`
3. If user confirms filename:
   - Opens file with CSV writer
   - Writes date row: `['Date', current_date, '', '', '']` (date without leading zeros)
   - Writes header row: `['Placement', 'Camera', 'Time', 'Side']`
   - Iterates table rows:
     - Gets time from column 0 item
     - Gets direction from column 1 combobox
     - Writes data row: `[row_number, 'Cam1', time, direction.lower()]`
   - Shows success message with file path

## Data Formats

### Time Format
- **Display**: HH:MM:SS (e.g., "00:01:23", "01:15:47")
- **Storage**: Milliseconds (integer) in QMediaPlayer
- **Conversion**: `format_time(ms)` converts ms to HH:MM:SS
- **Parsing**: `parse_time_to_ms(time_str)` converts HH:MM:SS to ms

### CSV Export Format
```
Date,2/23/2026,,,
Placement,Camera,Time,Side
1,Cam1,00:01:23,left
2,Cam1,00:02:15,right
3,Cam1,00:03:47,left
```

**Row Structure:**
- **Row 1**: Date header with current date (M/D/YYYY format, no leading zeros)
- **Row 2**: Column headers
- **Rows 3+**: Data rows with placement (1-indexed), camera (always "Cam1"), time (HH:MM:SS), side (lowercase)

## Menu Structure

### File Menu
- **Open Video** (Ctrl+O)
  - Opens QFileDialog for video file selection
  - Filters: "Video Files (*.mp4 *.avi *.mkv *.mov)"
  - Calls `load_video()` with selected path
  
- **Exit** (Ctrl+Q)
  - Closes application
  - Terminates all windows

### Tools Menu
- **Highlight CSV**
  - Creates HighlightCSVWindow if doesn't exist
  - Shows window (non-modal)
  - Window can be reopened if closed

### Help Menu
- **Check for Updates**
  - Queries `https://api.github.com/repos/{GITHUB_REPO}/releases/latest`
  - Parses JSON for `tag_name` (e.g., "v1.0.1")
  - Compares with current VERSION
  - Shows message box with result
  
- **About**
  - Displays modal QMessageBox with:
    - Application name
    - Version number
    - Description
    - Author: "Peter Barredo and his AI partner"
    - Keyboard shortcuts list

## Configuration Constants

Located at top of `player.py`:

```python
VERSION = "1.0.0"  # Semantic version (major.minor.patch)
GITHUB_REPO = "pvbarredo/pobre-media-player"  # GitHub username/repository
```

**Update for releases:** Increment VERSION before creating git tag.

## Build & Deployment

### GitHub Actions Workflow

**File:** `.github/workflows/release.yml`

**Trigger:** Push of tag matching `v*.*.*` pattern

**Jobs:**

1. **build-windows** (runs on windows-latest)
   - Checkout code
   - Setup Python 3.11
   - Install dependencies from requirements.txt
   - Install PyInstaller
   - Build: `pyinstaller --onefile --windowed --name="PobreMediaPlayer" player.py`
   - Upload artifact: `PobreMediaPlayer.exe`

2. **build-linux** (runs on ubuntu-20.04)
   - Checkout code
   - Setup Python 3.11
   - Install dependencies from requirements.txt
   - Install PyInstaller
   - Build: `pyinstaller --onefile --windowed --name="PobreMediaPlayer" player.py`
   - Set execute permissions: `chmod +x dist/PobreMediaPlayer`
   - Upload artifact: `PobreMediaPlayer`
   - **Note**: Uses Ubuntu 20.04 (GLIBC 2.31) for better compatibility with older Linux distributions

3. **create-release** (depends on build jobs)
   - Download both artifacts
   - Create GitHub release with tag
   - Attach Windows and Linux executables
   - Requires `permissions: contents: write`

### PyInstaller Flags

- `--onefile`: Bundle into single executable (no folder)
- `--windowed`: No console window (GUI application)
- `--name="PobreMediaPlayer"`: Output filename

## Implementation Details

### Focus Management

**Problem:** Interactive widgets (buttons, sliders) capture keyboard events, preventing shortcuts from working.

**Solution:** Set `QWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)` on:
- Play/pause button
- Position slider
- Volume slider

This ensures keyboard events always reach `keyPressEvent()` in main window.

### Drag-Drop on Nested Widgets

**Problem:** Placeholder widget inside stacked widget doesn't receive drop events by default.

**Solution:**
1. Set `setAcceptDrops(True)` on placeholder widget
2. Install event filter: `placeholder_widget.installEventFilter(self)`
3. Handle `QEvent.Type.DragEnter` and `QEvent.Type.Drop` in `eventFilter()` method
4. Forward events to main window's handlers

### Platform-Specific Date Formatting

**Issue:** Python's `strftime()` behaves differently on Windows vs Unix for removing leading zeros.

**Solution:**
```python
if os.name != 'nt':  # Unix/Linux/Mac
    date_str = datetime.now().strftime('%-m/%-d/%Y')  # Dash removes leading zero
else:  # Windows
    date_str = datetime.now().strftime('%#m/%#d/%Y')  # Hash removes leading zero
```

Result: Both produce "2/23/2026" instead of "02/23/2026"

### Non-Modal Window Management

**Requirement:** CSV window must stay accessible while controlling main player.

**Implementation:**
- Create HighlightCSVWindow with VideoPlayer as parent
- Use `show()` instead of `exec()` (exec makes modal)
- Store reference in VideoPlayer: `self.highlight_csv_window`
- Check reference exists before calling methods from keyboard shortcuts

**Benefit:** User can press 'S', 'L', 'R' keys in main window while CSV window is open.

## Design Decisions

### Why QStackedWidget Instead of show()/hide()?

**Advantages:**
- Smooth switching between widgets without flicker
- Both widgets maintained in memory (no re-creation overhead)
- Consistent size (both widgets occupy same space)
- Cleaner code: `setCurrentIndex(0)` vs `video.hide(); placeholder.show()`

### Why NoFocus on Control Widgets?

**User Experience:** Keyboard shortcuts are primary workflow. Users expect Space/Arrow keys to work immediately without clicking a specific area.

**Alternative Considered:** Custom event filter to intercept all key events before widgets process them. Rejected as overly complex.

### Why Hardcoded "Cam1" in CSV?

**Current Use Case:** Single camera video analysis
**Future Extension:** Could add camera selection dropdown in CSV table
**Simplicity:** Avoids UI complexity for most common use case

## Known Limitations

1. **Single Video:** Only one video at a time (no playlist)
2. **CSV Camera:** Always "Cam1", not customizable
3. **Codec Dependency:** Relies on system multimedia backends
4. **No Subtitle Support:** SRT/VTT files not supported
5. **No Fullscreen Mode:** Window can be maximized but no dedicated fullscreen

## File Structure

```
pobre-media-player/
├── .github/
│   └── workflows/
│       └── release.yml          # CI/CD workflow
├── prompt/
│   └── project_prompt.md       # This file - specifications
├── player.py                   # Main application (618 lines)
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── GETTING_STARTED.md         # Quick start guide
├── .gitignore                 # Git ignore patterns
└── dist/                      # PyInstaller output (gitignored)
```

## License

MIT License

## Credits

**Author:** Peter Barredo and his AI partner  
**Framework:** PyQt6 (Qt Group)  
**Language:** Python

---

*This document serves as the complete technical specification for Pobre Media Player.*
