#!/bin/bash
echo "Building Pobre Media Player for Linux..."
echo ""

# Install PyInstaller if not already installed
if ! pip show pyinstaller > /dev/null 2>&1; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

echo ""
echo "Building executable..."
pyinstaller --onefile --windowed --name=PobreMediaPlayer player.py

echo ""
echo "Build complete! Executable is in the dist/ folder."
echo ""
