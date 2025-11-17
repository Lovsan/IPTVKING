"""
IPTVking Pro - Main Entry Point
Advanced IPTV Player with Professional Features
"""

import sys
import os
import traceback
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from core.database import db_manager
from core.license_manager import license_manager
from ui.window.login_window import LoginWindow
from ui.window.main_window import MainWindow
from config.settings import AppConfig
import os

class IPTVKingApp:
    """Main application controller"""
    
    def __init__(self):
        self.app = None
        self.login_window = None
        self.main_window = None
        self.user_data = None
        
    def run(self):
        """Start the application"""
        try:
            # Setup application
            self.setup_application()
            
            # Show login window
            self.show_login()
            
            # Start event loop
            sys.exit(self.app.exec())
            
        except Exception as e:
            self.handle_critical_error(e)
    
    def setup_application(self):
        """Setup Qt application"""
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(AppConfig.APP_NAME)
        self.app.setApplicationVersion(AppConfig.APP_VERSION)
        self.app.setOrganizationName(AppConfig.COMPANY_NAME)
        
        # Set application-wide stylesheet
        self.app.setStyleSheet(AppConfig.get_theme_stylesheet())
        
        # Ensure directories exist
        AppConfig.setup_directories()
        
        print(f"🎬 {AppConfig.APP_NAME} v{AppConfig.APP_VERSION}")
        print(f"📁 Data directory: {AppConfig.DATA_DIR}")
    
    def show_login(self):
        """Show login window"""
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.on_login_success)
        self.login_window.show()
        
        # Auto-login for development
        if AppConfig.ENABLE_LICENSE:
            QTimer.singleShot(100, self.login_window.auto_login)
    
    def on_login_success(self, user_data):
        """Handle successful login"""
        self.user_data = user_data
        self.login_window.close()
        self.show_main_window()
    
    def show_main_window(self):
        """Show main application window"""
        try:
            self.main_window = MainWindow(
                username=self.user_data.get('username', 'Guest'),
                user_id=self.user_data.get('id')
            )
            self.main_window.show()
            
            # Show welcome message for new users
            if self.user_data.get('is_new_user', False):
                self.show_welcome_message()
                
        except Exception as e:
            self.handle_error("Failed to start main application", e)
    
    def show_welcome_message(self):
        """Show welcome message for new users"""
        QMessageBox.information(
            self.main_window,
            f"Welcome to {AppConfig.APP_NAME}!",
            "🎉 Welcome to IPTVking Pro!\n\n"
            "🚀 Getting Started:\n"
            "• Add playlists in the Content tab\n"
            "• Browse upcoming movies & TV shows\n"
            "• Request content you'd like to see\n"
            "• Manage your favorite channels\n\n"
            "💡 Pro Tip: Use 'DEV-MODE' as license key for all features!"
        )
    
    def handle_error(self, message, error):
        """Handle application errors"""
        print(f"❌ {message}: {error}")
        QMessageBox.warning(
            None,
            "Application Error",
            f"{message}\n\nError: {str(error)}"
        )
    
    def handle_critical_error(self, error):
        """Handle critical application errors"""
        error_msg = f"""
🚨 Critical Error in IPTVking Pro

Error: {str(error)}

Please ensure:
1. VLC media player is installed
2. You have write permissions in the application directory
3. Your system meets the minimum requirements

Technical details:
{traceback.format_exc()}
        """
        
        print(error_msg)
        QMessageBox.critical(
            None,
            "Fatal Error - IPTVking Pro",
            f"The application encountered a critical error and cannot continue.\n\n"
            f"Error: {str(error)}\n\n"
            f"Please check the console for more details."
        )
        sys.exit(1)

def main():
    """Application entry point"""
    app = IPTVKingApp()
    app.run()

if __name__ == '__main__':
    main()
