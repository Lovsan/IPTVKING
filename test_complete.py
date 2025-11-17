"""
Complete test suite for IPTVking multi-file structure
"""

import sys
import importlib
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_module_import(module_path: str) -> bool:
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_path)
        return True
    except Exception as e:
        print(f"❌ Failed to import {module_path}: {e}")
        return False

def test_class_instantiation(module_path: str, class_name: str) -> bool:
    """Test if a class can be instantiated"""
    try:
        module = importlib.import_module(module_path)
        class_obj = getattr(module, class_name)
        instance = class_obj()
        return True
    except Exception as e:
        print(f"❌ Failed to instantiate {class_name}: {e}")
        return False

def main():
    """Run complete test suite"""
    print("🧪 Running Complete IPTVking Test Suite\n")
    
    # Test modules and classes
    tests = [
        # Config
        ('config.settings', 'AppConfig', None),
        ('config.constants', None, None),
        
        # Core
        ('core.database', 'DatabaseManager', None),
        ('core.license_manager', 'LicenseManager', None),
        
        # Managers
        ('managers.content_manager', 'ContentManager', None),
        ('managers.favorites_manager', 'FavoritesManager', None),
        ('managers.playlist_manager', 'PlaylistManager', None),
        ('managers.user_manager', 'UserManager', None),
        
        # UI Components
        ('ui.components.widgets', 'ModernButton', None),
        ('ui.components.widgets', 'CardWidget', None),
        
        # Utils
        ('utils.helpers', None, None),
        ('utils.m3u_parser', 'M3UParser', None),
        
        # API
        ('api.local_server', 'LocalAPIServer', None),
        ('api.endpoints', 'APIEndpoints', None),
    ]
    
    passed = 0
    total = len(tests)
    
    for module_path, class_name, method_name in tests:
        print(f"Testing {module_path}...", end=" ")
        
        # Test module import
        if not test_module_import(module_path):
            continue
        
        # Test class instantiation if class specified
        if class_name and not test_class_instantiation(module_path, class_name):
            continue
        
        print("✅")
        passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! The structure is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)