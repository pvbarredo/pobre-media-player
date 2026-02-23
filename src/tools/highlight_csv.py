"""
Highlight CSV Tool - Create CSV files with video timestamps and direction markers
"""
import os
import csv
from datetime import datetime
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QMessageBox, QFileDialog, QStyle,
                              QTableWidget, QTableWidgetItem, QHeaderView, QComboBox)
from PyQt6.QtCore import QTimer


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
            self.statusBar().showMessage(
                f"Playing timestamp {self.current_playing_index + 1}/{self.table.rowCount()}: {time_str}",
                2000
            )
            
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
