"""
Script to create the complete project structure
"""

import os
import shutil
from pathlib import Path

def create_structure():
    """Create the complete project structure"""
    base_dir = Path(__file__).parent
    
    # Define the structure
    structure = {
        'config': ['__init__.py', 'settings.py', 'constants.py'],
        'core': ['__init__.py', 'database.py', 'license_manager.py'],
        'managers': ['__init__.py', 'content_manager.py', 'favorites_manager.py', 
                    'playlist_manager.py', 'user_manager.py'],
        'ui': {
            'components': ['__init__.py', 'widgets.py', 'cards.py'],
            'windows': ['__init__.py', 'main_window.py', 'login_window.py'],
            'tabs': ['__init__.py', 'content_tab.py', 'upcoming_tab.py', 
                    'requests_tab.py', 'favorites_tab.py', 'profile_tab.py', 'settings_tab.py']
        },
        'utils': ['__init__.py', 'helpers.py', 'm3u_parser.py', 'vlc_player.py'],
        'api': ['__init__.py', 'local_server.py', 'endpoints.py'],
        'data': ['playlists', 'recordings', 'cache']  # Directories only
    }
    
    # Create directories and files
    for item, contents in structure.items():
        item_path = base_dir / item
        
        if isinstance(contents, list):
            # It's a directory with files
            item_path.mkdir(exist_ok=True)
            for file in contents:
                if file.endswith('.py'):
                    # Create empty Python file
                    (item_path / file).touch()
                else:
                    # Create directory
                    (item_path / file).mkdir(exist_ok=True)
        else:
            # It's a nested structure
            item_path.mkdir(exist_ok=True)
    
    # Create main files
    main_files = ['main.py', 'requirements.txt', 'build_single_file.py', 
                 'test_app.py', 'run_dev.py', 'create_structure.py']
    
    for file in main_files:
        (base_dir / file).touch()
    
    print("✅ Project structure created successfully!")
    print("📁 Structure:")
    print_structure(base_dir)
    
    # Create requirements.txt content
    requirements = """python-vlc>=3.0.0
psutil>=5.9.0
requests>=2.28.0
PyQt6>=6.4.0
watchdog>=3.0.0  # For development auto-reload
"""
    
    with open(base_dir / 'requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("\n📋 Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Test the structure: python test_app.py")
    print("3. Run the app: python main.py")
    print("4. Develop with auto-reload: python run_dev.py")

def print_structure(base_dir: Path, prefix: str = ""):
    """Print the directory structure"""
    items = list(base_dir.iterdir())
    items.sort()
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        connector = "└── " if is_last else "├── "
        
        print(prefix + connector + item.name)
        
        if item.is_dir() and item.name not in ['data', '__pycache__', '.git']:
            extension = "    " if is_last else "│   "
            print_structure(item, prefix + extension)

if __name__ == '__main__':
    create_structure()