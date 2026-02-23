"""
Main Video Player Window
"""
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QSlider, QLabel, QFileDialog,
                              QMessageBox, QStyle, QSizePolicy, QStackedWidget)
from PyQt6.QtCore import Qt, QUrl, QEvent
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent, QKeyEvent
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

from ..config import VERSION, APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, CONTROLS_MAX_HEIGHT
from ..utils.updater import check_for_updates
from ..tools.highlight_csv import HighlightCSVWindow


class VideoPlayer(QMainWindow):
    """Main video player window with controls and menu"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
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
        controls_container.setMaximumHeight(CONTROLS_MAX_HEIGHT)
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(8, 3, 8, 3)
        controls_container.setLayout(controls_layout)
        
        # Play/Pause button
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
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
        self.position_slider.sliderPressed.connect(self.slider_pressed)
        self.position_slider.setFocusPolicy(Qt.FocusPolicy.NoFocus)
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
        self.volume_slider.setFocusPolicy(Qt.FocusPolicy.NoFocus)
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
        
        # Add footer label to status bar
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
        update_action.triggered.connect(lambda: check_for_updates(self))
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
            self.play_pause()
        elif event.key() == Qt.Key.Key_S:
            if self.highlight_csv_window:
                current_time = self.format_time(self.media_player.position())
                self.highlight_csv_window.add_row_with_time(current_time)
        elif event.key() == Qt.Key.Key_L:
            if self.highlight_csv_window:
                self.highlight_csv_window.update_last_direction("Left")
        elif event.key() == Qt.Key.Key_R:
            if self.highlight_csv_window:
                self.highlight_csv_window.update_last_direction("Right")
        elif event.key() == Qt.Key.Key_Left:
            current_pos = self.media_player.position()
            new_pos = max(0, current_pos - 3000)
            self.media_player.setPosition(new_pos)
        elif event.key() == Qt.Key.Key_Right:
            current_pos = self.media_player.position()
            duration = self.media_player.duration()
            new_pos = min(duration, current_pos + 3000)
            self.media_player.setPosition(new_pos)
        elif event.key() == Qt.Key.Key_Up:
            current_volume = self.volume_slider.value()
            new_volume = min(100, current_volume + 5)
            self.volume_slider.setValue(new_volume)
        elif event.key() == Qt.Key.Key_Down:
            current_volume = self.volume_slider.value()
            new_volume = max(0, current_volume - 5)
            self.volume_slider.setValue(new_volume)
        else:
            super().keyPressEvent(event)
            
    def show_about(self):
        """Show about dialog"""
        about_text = f"""
        <h2>{APP_NAME}</h2>
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
        QMessageBox.about(self, f"About {APP_NAME}", about_text)
    
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
