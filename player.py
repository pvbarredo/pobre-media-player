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
                              QFileDialog, QMessageBox, QStyle, QMenu, QSizePolicy,
                              QStackedWidget)
from PyQt6.QtCore import Qt, QTimer, QUrl, pyqtSignal, QEvent, QSize
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent, QKeyEvent, QPalette
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

VERSION = "1.0.0"
GITHUB_REPO = "pvbarredo/pobre-media-player"  


class VideoPlayer(QMainWindow):
    """Main video player window with controls and menu"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pobre Media Player")
        self.setGeometry(100, 100, 1280, 720)  # Larger window for better video display
        self.setAcceptDrops(True)
        
        # Initialize media player
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        
        # Video widget
        self.video_widget = QVideoWidget()
        self.video_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.video_widget.setAcceptDrops(True)
        self.video_widget.installEventFilter(self)  # Forward events to main window
        self.media_player.setVideoOutput(self.video_widget)
        
        # Placeholder widget for drag and drop
        self.placeholder_widget = QLabel()
        self.placeholder_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder_widget.setText("Drag and drop the video here to play")
        self.placeholder_widget.setStyleSheet("""
            QLabel {
                border: 3px dashed #888;
                border-radius: 10px;
                color: #888;
                font-size: 18px;
                font-weight: bold;
                background-color: #1a1a1a;
            }
        """)
        self.placeholder_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.placeholder_widget.setAcceptDrops(True)
        self.placeholder_widget.installEventFilter(self)
        
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
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for bigger video area
        layout.setSpacing(0)
        central_widget.setLayout(layout)
        
        # Stacked widget to switch between placeholder and video
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.stacked_widget.addWidget(self.placeholder_widget)  # Index 0
        self.stacked_widget.addWidget(self.video_widget)  # Index 1
        self.stacked_widget.setCurrentIndex(0)  # Show placeholder initially
        layout.addWidget(self.stacked_widget, 80)  # 80% of space for video
        
        # Control bar container
        controls_container = QWidget()
        controls_container.setMaximumHeight(120)  # Limit controls to ~20% of 720p window
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(10, 5, 10, 5)
        controls_container.setLayout(controls_layout)
        
        # Play/Pause button
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.clicked.connect(self.play_pause)
        controls_layout.addWidget(self.play_button)
        
        # Position label
        self.position_label = QLabel("00:00:00")
        self.position_label.setMinimumWidth(60)
        controls_layout.addWidget(self.position_label)
        
        # Progress slider
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.position_slider.sliderPressed.connect(self.slider_pressed)  # Jump when clicking
        self.position_slider.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Prevent arrow key capture
        controls_layout.addWidget(self.position_slider)
        
        # Duration label
        self.duration_label = QLabel("00:00:00")
        self.duration_label.setMinimumWidth(60)
        controls_layout.addWidget(self.duration_label)
        
        # Volume icon
        volume_icon = QLabel("🔊")
        controls_layout.addWidget(volume_icon)
        
        # Volume slider
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setMaximumWidth(100)
        self.volume_slider.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Prevent arrow key capture
        self.volume_slider.valueChanged.connect(self.change_volume)
        controls_layout.addWidget(self.volume_slider)
        
        # Volume label
        self.volume_label = QLabel("70%")
        self.volume_label.setMinimumWidth(35)
        controls_layout.addWidget(self.volume_label)
        
        # Set initial volume
        self.audio_output.setVolume(0.7)
        
        layout.addWidget(controls_container, 20)  # 20% of space for controls
        
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
            # Switch to video widget when loading video
            self.stacked_widget.setCurrentIndex(1)
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
        # Don't update slider if user is currently dragging it
        if not self.position_slider.isSliderDown():
            self.position_slider.setValue(position)
        self.position_label.setText(self.format_time(position))
        
    def duration_changed(self, duration):
        """Update duration slider range and label"""
        self.position_slider.setRange(0, duration)
        self.duration_label.setText(self.format_time(duration))
        
    def set_position(self, position):
        """Seek to position when slider is moved"""
        self.media_player.setPosition(position)
    
    def slider_pressed(self):
        """Jump to position when slider is clicked"""
        position = self.position_slider.sliderPosition()
        self.media_player.setPosition(position)
    
    def change_volume(self, value):
        """Change volume when slider is moved"""
        volume = value / 100.0
        self.audio_output.setVolume(volume)
        self.volume_label.setText(f"{value}%")
        
    def format_time(self, ms):
        """Format milliseconds to HH:MM:SS"""
        s = ms // 1000
        h = s // 3600
        m = (s % 3600) // 60
        s = s % 60
        return f"{h:02d}:{m:02d}:{s:02d}"
        
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
    
    def eventFilter(self, obj, event):
        """Event filter to handle drag and drop on video widget and placeholder"""
        if obj == self.video_widget or obj == self.placeholder_widget:
            if event.type() == QEvent.Type.DragEnter:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                    return True
            elif event.type() == QEvent.Type.Drop:
                files = [u.toLocalFile() for u in event.mimeData().urls()]
                if files:
                    file_path = files[0]
                    if file_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                        self.load_video(file_path)
                    else:
                        QMessageBox.warning(self, "Invalid File", "Please drop a valid video file (MP4, AVI, MKV, MOV)")
                return True
            elif event.type() == QEvent.Type.KeyPress:
                # Forward keyboard events to main window
                self.keyPressEvent(event)
                return True
        return super().eventFilter(obj, event)
    
    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard shortcuts"""
        if event.key() == Qt.Key.Key_Space:
            # Space: Play/Pause
            self.play_pause()
        elif event.key() == Qt.Key.Key_Left:
            # Left arrow: Rewind 3 seconds
            current_pos = self.media_player.position()
            new_pos = max(0, current_pos - 3000)  # 3 seconds = 3000ms
            self.media_player.setPosition(new_pos)
        elif event.key() == Qt.Key.Key_Right:
            # Right arrow: Forward 3 seconds
            current_pos = self.media_player.position()
            duration = self.media_player.duration()
            new_pos = min(duration, current_pos + 3000)  # 3 seconds = 3000ms
            self.media_player.setPosition(new_pos)
        elif event.key() == Qt.Key.Key_Up:
            # Up arrow: Increase volume
            current_volume = self.volume_slider.value()
            new_volume = min(100, current_volume + 5)
            self.volume_slider.setValue(new_volume)
        elif event.key() == Qt.Key.Key_Down:
            # Down arrow: Decrease volume
            current_volume = self.volume_slider.value()
            new_volume = max(0, current_volume - 5)
            self.volume_slider.setValue(new_volume)
        else:
            super().keyPressEvent(event)
                
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
            <li>MP4 video playback with maximized display (80% window)</li>
            <li>Drag and drop anywhere in the app</li>
            <li>Visual placeholder with instructions</li>
            <li>Compact controls (20% window height)</li>
            <li>Play, pause, and instant seek controls</li>
            <li>Volume control with slider</li>
            <li>Time display in HH:MM:SS format</li>
            <li>Keyboard shortcuts (Space, Arrow keys)</li>
            <li>Auto-update checker</li>
        </ul>
        <p><b>Keyboard Shortcuts:</b></p>
        <ul>
            <li>Space: Play/Pause</li>
            <li>Left/Right Arrow: Skip -3/+3 seconds</li>
            <li>Up/Down Arrow: Volume +/-</li>
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
