from PyQt6.QtWidgets import QMainWindow, QTabWidget, QStatusBar
from PyQt6.QtCore import pyqtSignal

from ui.tabs.content_tab import ContentTab
from ui.tabs.upcoming_tab import UpcomingTab
from ui.tabs.requests_tab import RequestsTab
from ui.tabs.favorites_tab import FavoritesTab
from ui.tabs.profile_tab import ProfileTab
from ui.tabs.settings_tab import SettingsTab

class MainWindow(QMainWindow):
    """Main application window with tabbed interface."""

    def __init__(self, username="Guest", user_id=None, parent=None):
        super().__init__(parent)
        self.username = username
        self.user_id = user_id

        self.setWindowTitle(f"IPTVking Pro - {username}")
        self.setGeometry(100, 100, 1400, 900)

        # Create the tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Initialize tabs
        self.content_tab = ContentTab(self)
        self.upcoming_tab = UpcomingTab(self)
        self.requests_tab = RequestsTab(self)
        self.favorites_tab = FavoritesTab(self)
        self.profile_tab = ProfileTab(self)
        self.settings_tab = SettingsTab(self)

        # Add tabs to the tab widget
        self.tab_widget.addTab(self.content_tab, "Content")
        self.tab_widget.addTab(self.upcoming_tab, "Upcoming")
        self.tab_widget.addTab(self.requests_tab, "Requests")
        self.tab_widget.addTab(self.favorites_tab, "Favorites")
        self.tab_widget.addTab(self.profile_tab, "Profile")
        self.tab_widget.addTab(self.settings_tab, "Settings")

        # Set up status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Show status message
        self.status_bar.showMessage("Ready")

    def show_status_message(self, message, timeout=5000):
        """Show a message in the status bar."""
        self.status_bar.showMessage(message, timeout)