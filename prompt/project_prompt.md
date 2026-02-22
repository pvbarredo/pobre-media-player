# Pobre Media Player - Project Prompt

## Overview
A lightweight, portable media player built with Python that supports MP4 video playback with basic controls.

## Key Features
- Cross-platform support (Windows & Linux)
- MP4 video playback
- Basic controls: Play, Pause, Seek (click on progress bar)
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
- Main window with video display area
- Control bar with play/pause button
- Progress bar with seek functionality
- Menu bar with File, Tools, and Help menus

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
