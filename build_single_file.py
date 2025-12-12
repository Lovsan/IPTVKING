"""
Enhanced build script to create a single-file version
"""

import re
from pathlib import Path
from typing import Set, List

class SingleFileBuilder:
    """Builds a single Python file from the multi-file structure"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.output_file = self.project_root / "iptvking_single.py"
        self.processed_files: Set[Path] = set()
        self.import_map = {}
        
    def build(self):
        """Build the single file"""
        print("🚀 Building single file version...")
        
        # Start with main.py
        final_content = self.process_file(self.project_root / "main.py")
        
        # Write the single file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_header())
            f.write(final_content)
        
        print(f"✅ Single file built: {self.output_file}")
        print(f"📊 Processed {len(self.processed_files)} files")
        
        # Print file statistics
        self.print_stats()
    
    def generate_header(self):
        """Generate file header"""
        return '''"""
IPTVking Pro - Single File Version
Advanced IPTV Player with Professional Features

Auto-generated from multi-file structure.
For development, use the multi-file version.

Requirements:
- python-vlc
- psutil  
- requests
- PyQt6
"""

'''
    
    def process_file(self, file_path: Path) -> str:
        """Process a file and its imports"""
        if file_path in self.processed_files:
            return ""
        
        self.processed_files.add(file_path)
        print(f"📄 Processing: {file_path.relative_to(self.project_root)}")
        
        content = self.read_file(file_path)
        
        # Remove shebang and encoding comments
        content = re.sub(r'^#!/usr/bin/env python3\s*\n', '', content)
        content = re.sub(r'^# -\*- coding: utf-8 -\*-\s*\n', '', content)
        
        # Process imports and replace with actual code
        processed_content = self.process_imports(content, file_path)
        
        return processed_content
    
    def process_imports(self, content: str, current_file: Path) -> str:
        """Process imports in file content"""
        lines = content.split('\n')
        processed_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Skip empty __init__.py files
            if (current_file.name == '__init__.py' and 
                line.strip() in ['', '# Package initialization', '# Package']):
                i += 1
                continue
                
            # Handle imports
            if line.startswith(('from ', 'import ')) and not line.startswith('from typing'):
                # Check if it's a local import
                if self.is_local_import(line):
                    imported_content = self.handle_local_import(line, current_file)
                    if imported_content:
                        processed_lines.append(f"\n# === Content from {line.strip()} ===")
                        processed_lines.append(imported_content)
                        processed_lines.append(f"# === End of {line.strip()} ===\n")
                else:
                    # Keep external imports
                    processed_lines.append(line)
            else:
                # Keep regular lines
                processed_lines.append(line)
            
            i += 1
        
        return '\n'.join(processed_lines)
    
    def is_local_import(self, import_line: str) -> bool:
        """Check if import is local to our project"""
        local_modules = ['config', 'core', 'managers', 'ui', 'utils', 'api']
        
        if import_line.startswith('from '):
            module = import_line.split()[1]
            return any(module.startswith(local) for local in local_modules)
        elif import_line.startswith('import '):
            modules = [m.strip() for m in import_line[7:].split(',')]
            return any(any(m.startswith(local) for local in local_modules) for m in modules)
        
        return False
    
    def handle_local_import(self, import_line: str, current_file: Path) -> str:
        """Handle local import by including the imported file"""
        if import_line.startswith('from '):
            # Handle 'from module import something'
            parts = import_line.split()
            module_path = parts[1]
            
            
            # Convert module path to file path
            file_path = self.module_to_file(module_path, current_file)
            if file_path and file_path.exists():
                return self.process_file(file_path)
        
        return ""
    
    def module_to_file(self, module_path: str, current_file: Path) -> Path:
        """Convert module path to file path"""
        parts = module_path.split('.')
        
        # Try relative to current file first
        relative_path = current_file.parent
        for part in parts:
            relative_path = relative_path / part
        
        # Try different extensions
        for ext in ['.py', '/__init__.py']:
            test_path = Path(str(relative_path) + ext)
            if test_path.exists():
                return test_path
        
        # Try from project root
        project_path = self.project_root
        for part in parts:
            project_path = project_path / part
        
        for ext in ['.py', '/__init__.py']:
            test_path = Path(str(project_path) + ext)
            if test_path.exists():
                return test_path
        
        return None
    
    def read_file(self, file_path: Path) -> str:
        """Read file content with error handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return ""
    
    def print_stats(self):
        """Print build statistics"""
        file_types = {}
        total_lines = 0
        
        for file_path in self.processed_files:
            ext = file_path.suffix
            file_types[ext] = file_types.get(ext, 0) + 1
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    total_lines += len(f.readlines())
            except Exception:
                pass
        
        print(f"📈 Statistics:")
        print(f"   Total files: {len(self.processed_files)}")
        print(f"   Total lines: ~{total_lines}")
        print(f"   File types: {file_types}")

def main():
    """Build the single file"""
    builder = SingleFileBuilder()
    builder.build()

if __name__ == '__main__':
    main()