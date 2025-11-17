"""
Development runner script with auto-reload and debugging
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DevReloadHandler(FileSystemEventHandler):
    """Handler for file changes during development"""
    
    def __init__(self, script_path):
        self.script_path = script_path
        self.process = None
        self.restart()
    
    def on_modified(self, event):
        """Restart when Python files change"""
        if event.src_path.endswith('.py'):
            print(f"\n🔄 File changed: {Path(event.src_path).name}")
            self.restart()
    
    def restart(self):
        """Restart the application"""
        if self.process:
            self.process.terminate()
            self.process.wait()
        
        print("🚀 Starting IPTVking...")
        self.process = subprocess.Popen([sys.executable, self.script_path])
    
    def stop(self):
        """Stop the application"""
        if self.process:
            self.process.terminate()
            self.process.wait()

def main():
    """Run development server with auto-reload"""
    script_path = Path(__file__).parent / "main.py"
    
    if not script_path.exists():
        print("❌ main.py not found!")
        return
    
    print("🎬 Starting IPTVking Development Server")
    print("   Auto-reload enabled - files will reload on changes")
    print("   Press Ctrl+C to stop\n")
    
    # Check dependencies
    try:
        import watchdog
    except ImportError:
        print("⚠️  Install watchdog for auto-reload: pip install watchdog")
        # Run without auto-reload
        subprocess.run([sys.executable, str(script_path)])
        return
    
    # Start with auto-reload
    event_handler = DevReloadHandler(script_path)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️  Stopping development server...")
        observer.stop()
        event_handler.stop()
    
    observer.join()

if __name__ == '__main__':
    main()