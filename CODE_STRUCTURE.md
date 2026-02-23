# Code Structure

This project has been refactored into a modular architecture for better maintainability and scalability.

## Directory Structure

```
pobre-media-player/
├── player.py              # Main entry point
├── requirements.txt       # Python dependencies
├── src/                   # Source code modules
│   ├── __init__.py
│   ├── config.py          # Configuration and constants
│   ├── player/            # Video player components
│   │   ├── __init__.py
│   │   └── video_player.py   # Main VideoPlayer class
│   ├── tools/             # Video analysis tools
│   │   ├── __init__.py
│   │   └── highlight_csv.py  # Highlight CSV tool
│   └── utils/             # Utility functions
│       ├── __init__.py
│       └── updater.py     # Update checker
├── build.bat/sh           # Build scripts
├── run.bat/sh             # Run scripts
└── .github/workflows/     # CI/CD workflows
```

## Module Descriptions

### `src/config.py`
Contains application constants and configuration:
- `VERSION` - Application version
- `GITHUB_REPO` - GitHub repository for updates
- `APP_NAME` - Application name
- Window dimensions and UI constants

### `src/player/video_player.py`
Main video player window class:
- Video playback controls
- Drag and drop support
- Keyboard shortcuts
- Menu system
- Media player integration

### `src/tools/highlight_csv.py`
Highlight CSV tool for video analysis:
- Timestamp recording
- Direction markers (Left/Right)
- CSV export functionality
- Playback of recorded timestamps

### `src/utils/updater.py`
Update checker utility:
- Checks GitHub releases for new versions
- Displays update notifications
- Provides download links

## Adding New Tools

To add a new video analysis tool:

1. Create a new file in `src/tools/`:
   ```python
   # src/tools/your_tool.py
   from PyQt6.QtWidgets import QMainWindow
   
   class YourToolWindow(QMainWindow):
       def __init__(self, parent=None):
           super().__init__(parent)
           self.player = parent
           # Your tool implementation
   ```

2. Add import to `src/tools/__init__.py`:
   ```python
   from .your_tool import YourToolWindow
   __all__ = ['HighlightCSVWindow', 'YourToolWindow']
   ```

3. Add menu item in `src/player/video_player.py`:
   ```python
   from ..tools import YourToolWindow
   
   # In create_menu_bar():
   your_tool_action = QAction("&Your Tool", self)
   your_tool_action.triggered.connect(self.open_your_tool)
   tools_menu.addAction(your_tool_action)
   ```

## Benefits of This Structure

- **Modularity**: Each component is in its own file
- **Maintainability**: Easy to find and update specific features
- **Scalability**: Simple to add new tools without cluttering main code
- **Testability**: Individual modules can be tested independently
- **Readability**: Clear separation of concerns

## Migration Notes

The original monolithic `player.py` has been backed up as `player_old.py` and can be removed once the refactored version is verified to work correctly.
