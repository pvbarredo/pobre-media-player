# Source Code Organization

This directory contains the modular components of Pobre Media Player.

## Quick Reference

```
src/
├── config.py           # ⚙️  Configuration & Constants
├── player/             # 🎬 Video Player Components
│   ├── video_player.py    # Main player window
│   └── __init__.py
├── tools/              # 🛠️  Video Analysis Tools
│   ├── highlight_csv.py   # CSV timestamp tool
│   └── __init__.py
└── utils/              # 🔧 Utility Functions
    ├── updater.py         # GitHub update checker
    └── __init__.py
```

## Import Examples

```python
# From main application (player.py)
from src.config import VERSION, APP_NAME
from src.player import VideoPlayer

# From a tool
from src.config import VERSION
from src.utils.updater import check_for_updates

# Add a new tool to the tools menu
from src.tools import YourNewTool
```

## Module Details

### Config (`config.py`)
Central configuration file for application-wide constants:
- Version number
- Application name
- GitHub repository
- UI dimensions

### Player (`player/`)
Core video player functionality:
- **video_player.py**: Main application window with playback controls, menus, and keyboard shortcuts

### Tools (`tools/`)
Extensible video analysis tools:
- **highlight_csv.py**: Record timestamps with direction markers, export to CSV
- *Future tools can be added here*

### Utils (`utils/`)
Reusable utility functions:
- **updater.py**: Check for application updates from GitHub

## Best Practices

1. **Add constants to `config.py`** instead of hardcoding values
2. **Create new tools in `tools/`** as separate files
3. **Put reusable functions in `utils/`**
4. **Update `__init__.py`** when adding new modules
5. **Keep imports relative** within src/ (use `from ..config import`)
