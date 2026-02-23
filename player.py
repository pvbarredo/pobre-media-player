#!/usr/bin/env python3
"""
Pobre Media Player - A lightweight, portable MP4 video player

Entry point for the application.
For code organization, see the src/ directory:
- src/config.py - Configuration and constants
- src/player/ - Main video player components
- src/tools/ - Video analysis tools (Highlight CSV, etc.)
- src/utils/ - Utility functions (updater, etc.)
"""

import sys
from PyQt6.QtWidgets import QApplication

from src.config import VERSION, APP_NAME
from src.player import VideoPlayer


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(VERSION)
    
    player = VideoPlayer()
    player.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
