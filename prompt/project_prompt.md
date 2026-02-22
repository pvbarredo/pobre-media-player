# Pobre Media Player - Project Prompt

## Overview
A lightweight, portable media player built with Python that supports MP4 video playback with basic controls.

## Key Features
- Cross-platform support (Windows & Linux)
- MP4 video playback
- Basic controls: Play, Pause, Seek (click on progress bar)
- Volume control with slider
- Keyboard shortcuts for playback and volume control
- Drag and drop support for MP4 files
- Menu bar: File, Tools, Help
- Auto-update checker (GitHub releases)
- Portable executable

## Technical Stack
- Python 3.8+
- PyQt6 for UI
- python-vlc for media playback
- requests for update checking

## User Interface
- Main window with maximized video display area (80% of window)
- Visual placeholder with dashed border and instructions when no video is loaded
- Compact control bar at bottom (20% of window height)
- Play/pause button
- Progress bar with seek functionality and instant jump on click
- Time display in HH:MM:SS format
- Volume slider with percentage display
- Menu bar with File, Tools, and Help menus

## Keyboard Shortcuts
- **Space**: Toggle play/pause
- **Left Arrow**: Rewind 3 seconds
- **Right Arrow**: Forward 3 seconds
- **Up Arrow**: Increase volume by 5%
- **Down Arrow**: Decrease volume by 5%
- **Ctrl+O**: Open video file
- **Ctrl+Q**: Exit application

## Menu Structure
### File
- Open Video
- Exit

### Tools
- (Future features)

### Help
- Check for Updates
- About

## Update Mechanism
- Checks GitHub releases API
- Compares current version with latest release
- Notifies user of available updates
