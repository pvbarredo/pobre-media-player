"""
Update checker for Pobre Media Player
"""
import requests
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

from ..config import VERSION, GITHUB_REPO


def check_for_updates(parent_window):
    """
    Check for updates from GitHub releases
    
    Args:
        parent_window: The parent QMainWindow for displaying dialogs
    """
    try:
        parent_window.statusBar().showMessage("Checking for updates...")
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release.get("tag_name", "").lstrip("v")
            
            if latest_version and latest_version != VERSION:
                download_url = latest_release.get('html_url', '')
                message = f"<b>New version available: {latest_version}</b><br>"
                message += f"Current version: {VERSION}<br><br>"
                message += f"Download from:<br>"
                message += f'<a href="{download_url}">{download_url}</a>'
                
                msg_box = QMessageBox(parent_window)
                msg_box.setWindowTitle("Update Available")
                msg_box.setTextFormat(Qt.TextFormat.RichText)
                msg_box.setText(message)
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.exec()
                
                parent_window.statusBar().showMessage("Update available!")
            else:
                QMessageBox.information(
                    parent_window,
                    "No Updates",
                    f"You are using the latest version ({VERSION})"
                )
                parent_window.statusBar().showMessage("Up to date")
        else:
            QMessageBox.warning(
                parent_window,
                "Update Check Failed",
                "Could not check for updates. Please try again later."
            )
            parent_window.statusBar().showMessage("Update check failed")
            
    except requests.RequestException as e:
        QMessageBox.warning(
            parent_window,
            "Network Error",
            f"Could not connect to update server:\n{str(e)}"
        )
        parent_window.statusBar().showMessage("Update check failed")
    except Exception as e:
        QMessageBox.warning(
            parent_window,
            "Error",
            f"An error occurred:\n{str(e)}"
        )
        parent_window.statusBar().showMessage("Update check failed")
