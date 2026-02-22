#!/usr/bin/env python3
"""
Pobre Media Player - A lightweight, portable MP4 video player
Version: 1.0.0
"""

import sys
import os
import requests
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QSlider, QLabel, 
                              QFileDialog, QMessageBox, QStyle, QMenu)
from PyQt6.QtCore import Qt, QTimer, QUrl, pyqtSignal
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

VERSION = "1.0.0"
GITHUB_REPO = "pvbarredo/pobre-media-player"  


class VideoPlayer(QMainWindow):
    """Main video player window with controls and menu"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pobre Media Player")
        self.setGeometry(100, 100, 800, 600)
        self.setAcceptDrops(True)
        
        # Initialize media player
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        
        # Video widget
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)
        
        # Setup UI
        self.init_ui()
        self.create_menu_bar()
        
        # Connect signals
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.playbackStateChanged.connect(self.state_changed)
        
    def init_ui(self):
        """Initialize the user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Video widget
        layout.addWidget(self.video_widget)
        
        # Control bar
        controls_layout = QHBoxLayout()
        
        # Play/Pause button
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.clicked.connect(self.play_pause)
        controls_layout.addWidget(self.play_button)
        
        # Position label
        self.position_label = QLabel("00:00")
        controls_layout.addWidget(self.position_label)
        
        # Progress slider
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)
        controls_layout.addWidget(self.position_slider)
        
        # Duration label
        self.duration_label = QLabel("00:00")
        controls_layout.addWidget(self.duration_label)
        
        layout.addLayout(controls_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready - Drag and drop an MP4 file to play")
        
    def create_menu_bar(self):
        """Create menu bar with File, Tools, and Help menus"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open Video", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        tools_menu.addAction("(Future features)")
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        update_action = QAction("Check for &Updates", self)
        update_action.triggered.connect(self.check_for_updates)
        help_menu.addAction(update_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def open_file(self):
        """Open file dialog to select video"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Video File",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov);;MP4 Files (*.mp4);;All Files (*.*)"
        )
        
        if file_name:
            self.load_video(file_name)
            
    def load_video(self, file_path):
        """Load and play video file"""
        if os.path.exists(file_path):
            self.media_player.setSource(QUrl.fromLocalFile(file_path))
            self.media_player.play()
            self.statusBar().showMessage(f"Playing: {os.path.basename(file_path)}")
        else:
            QMessageBox.warning(self, "Error", "File not found!")
            
    def play_pause(self):
        """Toggle play/pause state"""
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()
            
    def state_changed(self, state):
        """Update UI when playback state changes"""
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            
    def position_changed(self, position):
        """Update position slider and label"""
        self.position_slider.setValue(position)
        self.position_label.setText(self.format_time(position))
        
    def duration_changed(self, duration):
        """Update duration slider range and label"""
        self.position_slider.setRange(0, duration)
        self.duration_label.setText(self.format_time(duration))
        
    def set_position(self, position):
        """Seek to position when slider is moved"""
        self.media_player.setPosition(position)
        
    def format_time(self, ms):
        """Format milliseconds to MM:SS"""
        s = ms // 1000
        m = s // 60
        s = s % 60
        return f"{m:02d}:{s:02d}"
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        """Handle drop event for video files"""
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            file_path = files[0]
            # Check if it's a video file
            if file_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                self.load_video(file_path)
            else:
                QMessageBox.warning(self, "Invalid File", "Please drop a valid video file (MP4, AVI, MKV, MOV)")
                
    def check_for_updates(self):
        """Check for updates from GitHub releases"""
        try:
            self.statusBar().showMessage("Checking for updates...")
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release.get("tag_name", "").lstrip("v")
                
                if latest_version and latest_version != VERSION:
                    message = f"New version available: {latest_version}\n"
                    message += f"Current version: {VERSION}\n\n"
                    message += f"Download URL:\n{latest_release.get('html_url', '')}"
                    QMessageBox.information(self, "Update Available", message)
                    self.statusBar().showMessage("Update available!")
                else:
                    QMessageBox.information(self, "No Updates", f"You are using the latest version ({VERSION})")
                    self.statusBar().showMessage("Up to date")
            else:
                QMessageBox.warning(self, "Update Check Failed", "Could not check for updates. Please try again later.")
                self.statusBar().showMessage("Update check failed")
                
        except requests.RequestException as e:
            QMessageBox.warning(self, "Network Error", f"Could not connect to update server:\n{str(e)}")
            self.statusBar().showMessage("Update check failed")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred:\n{str(e)}")
            self.statusBar().showMessage("Error checking updates")
            
    def show_about(self):
        """Show about dialog"""
        about_text = f"""
        <h2>Pobre Media Player</h2>
        <p><b>Version:</b> {VERSION}</p>
        <p><b>Description:</b> A lightweight, portable media player for Windows and Linux</p>
        <p><b>Features:</b></p>
        <ul>
            <li>MP4 video playback</li>
            <li>Drag and drop support</li>
            <li>Basic playback controls</li>
            <li>Auto-update checker</li>
        </ul>
        <p><b>License:</b> MIT</p>
        <p><b>GitHub:</b> <a href="https://github.com/{GITHUB_REPO}">github.com/{GITHUB_REPO}</a></p>
        """
        QMessageBox.about(self, "About Pobre Media Player", about_text)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Pobre Media Player")
    app.setApplicationVersion(VERSION)
    
    player = VideoPlayer()
    player.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
