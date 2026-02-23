#!/usr/bin/env python3
"""
Pobre Media Player - A lightweight, portable MP4 video player
"""

import sys
import os
import csv
import requests
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QSlider, QLabel, 
                              QFileDialog, QMessageBox, QStyle, QMenu, QSizePolicy,
                              QStackedWidget, QTableWidget, QTableWidgetItem, 
                              QHeaderView, QDialog, QComboBox)
from PyQt6.QtCore import Qt, QTimer, QUrl, pyqtSignal, QEvent, QSize
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent, QKeyEvent, QPalette
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

VERSION = "1.0.6"
GITHUB_REPO = "pvbarredo/pobre-media-player"  


class VideoPlayer(QMainWindow):
    """Main video player window with controls and menu"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pobre Media Player")
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
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
        
        # Highlight CSV window reference
        self.highlight_csv_window = None
        
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
        layout.addWidget(self.stacked_widget, 90)  # 90% of space for video
        
        # Control bar container
        controls_container = QWidget()
        controls_container.setMaximumHeight(72)  # Limit controls to ~10% of 720p window
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(8, 3, 8, 3)
        controls_container.setLayout(controls_layout)
        
        # Play/Pause button
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Prevent button from capturing arrow keys
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
        
        layout.addWidget(controls_container, 10)  # 10% of space for controls
        
        # Status bar with footer
        self.statusBar().showMessage("Ready - Drag and drop an MP4 file to play")
        
        # Add footer label to status bar (permanent widget on the right)
        footer_label = QLabel("Pedro Barredo @ 2026")
        footer_label.setStyleSheet("color: #888; padding-right: 10px;")
        self.statusBar().addPermanentWidget(footer_label)
        
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
        
        highlight_csv_action = QAction("&Highlight CSV", self)
        highlight_csv_action.triggered.connect(self.open_highlight_csv)
        tools_menu.addAction(highlight_csv_action)
        
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
        elif event.key() == Qt.Key.Key_S:
            # S key: Add current time to Highlight CSV
            if self.highlight_csv_window:
                current_time = self.format_time(self.media_player.position())
                self.highlight_csv_window.add_row_with_time(current_time)
        elif event.key() == Qt.Key.Key_L:
            # L key: Set last row direction to Left
            if self.highlight_csv_window:
                self.highlight_csv_window.update_last_direction("Left")
        elif event.key() == Qt.Key.Key_R:
            # R key: Set last row direction to Right
            if self.highlight_csv_window:
                self.highlight_csv_window.update_last_direction("Right")
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
        <p><b>Author:</b> Peter Barredo and his AI partner</p>
        <p><b>Keyboard Shortcuts:</b></p>
        <ul>
            <li>Space: Play/Pause</li>
            <li>S: Add current time to Highlight CSV</li>
            <li>L/R: Set last CSV row to Left/Right</li>
            <li>Left/Right Arrow: Skip -3/+3 seconds</li>
            <li>Up/Down Arrow: Volume +/-</li>
        </ul>
        """
        QMessageBox.about(self, "About Pobre Media Player", about_text)
    
    def open_highlight_csv(self):
        """Open the Highlight CSV window"""
        if self.highlight_csv_window is None:
            self.highlight_csv_window = HighlightCSVWindow(self)
            self.highlight_csv_window.show()
        else:
            # If window already exists, just bring it to front
            self.highlight_csv_window.show()
            self.highlight_csv_window.raise_()
            self.highlight_csv_window.activateWindow()


class HighlightCSVWindow(QMainWindow):
    """Non-modal window for creating highlight CSV with timestamps and directions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Highlight CSV")
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView))
        self.setGeometry(200, 200, 600, 400)
        
        # Store parent reference for video control
        self.player = parent
        self.current_playing_index = -1
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.check_play_next)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Top row with Save button
        top_layout = QHBoxLayout()
        self.save_button = QPushButton("Save CSV")
        self.save_button.clicked.connect(self.save_csv)
        top_layout.addWidget(self.save_button)
        
        # Play All button
        self.play_all_button = QPushButton("Play All")
        self.play_all_button.clicked.connect(self.play_all_timestamps)
        top_layout.addWidget(self.play_all_button)
        
        top_layout.addStretch()
        layout.addLayout(top_layout)
        
        # Add row button
        add_button = QPushButton("Add Row")
        add_button.clicked.connect(self.add_row)
        top_layout.addWidget(add_button)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Time", "Direction"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        # Add initial empty row
        self.add_row()
    
    def add_row(self, time_value="00:00:00"):
        """Add a new row to the table"""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        # Time cell (editable)
        time_item = QTableWidgetItem(time_value)
        self.table.setItem(row_position, 0, time_item)
        
        # Direction cell (combo box)
        direction_combo = QComboBox()
        direction_combo.addItems(["Left", "Right"])
        self.table.setCellWidget(row_position, 1, direction_combo)
    
    def add_row_with_time(self, time_value):
        """Add a new row with specific time value"""
        self.add_row(time_value)
        # Scroll to the new row
        self.table.scrollToBottom()
        # Flash or highlight to show it was added
        self.statusBar().showMessage(f"Added timestamp: {time_value}", 2000)
    
    def save_csv(self):
        """Save the table data to a CSV file"""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save CSV File",
            f"highlights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv);;All Files (*.*)"
        )
        
        if file_name:
            try:
                with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write date header row
                    current_date = datetime.now().strftime('%-m/%-d/%Y') if os.name != 'nt' else datetime.now().strftime('%#m/%#d/%Y')
                    writer.writerow(['Date', current_date, '', '', ''])
                    
                    # Write column headers
                    writer.writerow(['Placement', 'Camera', 'Time', 'Side'])
                    
                    # Write data
                    for row in range(self.table.rowCount()):
                        time_item = self.table.item(row, 0)
                        direction_widget = self.table.cellWidget(row, 1)
                        
                        if time_item and direction_widget:
                            placement = row + 1
                            camera = "Cam1"
                            time = time_item.text()
                            side = direction_widget.currentText().lower()
                            writer.writerow([placement, camera, time, side])
                
                QMessageBox.information(self, "Success", f"CSV file saved to:\n{file_name}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save CSV:\n{str(e)}")
    
    def update_last_direction(self, direction):
        """Update the direction of the last row in the table"""
        row_count = self.table.rowCount()
        if row_count > 0:
            last_row = row_count - 1
            direction_widget = self.table.cellWidget(last_row, 1)
            if direction_widget:
                index = 0 if direction == "Left" else 1
                direction_widget.setCurrentIndex(index)
                self.statusBar().showMessage(f"Updated last row to: {direction}", 2000)
    
    def parse_time_to_ms(self, time_str):
        """Convert HH:MM:SS time string to milliseconds"""
        try:
            parts = time_str.split(':')
            if len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
                return (hours * 3600 + minutes * 60 + seconds) * 1000
        except:
            pass
        return 0
    
    def play_all_timestamps(self):
        """Play video at each recorded timestamp sequentially"""
        if not self.player:
            QMessageBox.warning(self, "Error", "No video player found!")
            return
        
        row_count = self.table.rowCount()
        if row_count == 0:
            QMessageBox.information(self, "No Data", "No timestamps to play!")
            return
        
        # Start playing from first timestamp
        self.current_playing_index = 0
        self.play_current_timestamp()
        self.statusBar().showMessage("Playing all timestamps...")
    
    def play_current_timestamp(self):
        """Play the video at current timestamp index"""
        if self.current_playing_index >= self.table.rowCount():
            self.statusBar().showMessage("Finished playing all timestamps", 3000)
            self.current_playing_index = -1
            self.play_timer.stop()
            return
        
        # Get time from current row
        time_item = self.table.item(self.current_playing_index, 0)
        if time_item:
            time_str = time_item.text()
            time_ms = self.parse_time_to_ms(time_str)
            
            # Seek to timestamp
            self.player.media_player.setPosition(time_ms)
            
            # Highlight current row
            self.table.selectRow(self.current_playing_index)
            
            # Show status
            self.statusBar().showMessage(f"Playing timestamp {self.current_playing_index + 1}/{self.table.rowCount()}: {time_str}", 2000)
            
            # Start timer to play next (wait 3 seconds at each timestamp)
            self.play_timer.start(3000)
    
    def check_play_next(self):
        """Check and play next timestamp"""
        self.play_timer.stop()
        self.current_playing_index += 1
        self.play_current_timestamp()
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Clear the reference in parent window
        if self.parent():
            self.parent().highlight_csv_window = None
        event.accept()


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
