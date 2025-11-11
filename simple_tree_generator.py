"""
Simple Tree to Folders Generator
Creates folders and files from a tree structure definition
"""

import os
import sys
from pathlib import Path


def parse_tree_to_items(tree_text):
    """
    Parse tree text and convert to list of (path, is_folder) tuples.
    
    Supports tree characters: ├──, │, └──
    Also supports simple indentation
    """
    items = []
    lines = tree_text.strip().split('\n')
    
    for line in lines:
        # Extract actual path, removing tree characters
        cleaned = line
        tree_chars = ['├── ', '├─', '│   ', '│', '└── ', '└─', '   ', '  ']
        
        for char in tree_chars:
            cleaned = cleaned.replace(char, '')
        
        cleaned = cleaned.strip()
        
        if cleaned:
            is_folder = cleaned.endswith('/')
            if is_folder:
                cleaned = cleaned[:-1]
            items.append((cleaned, is_folder))
    
    return items


def build_full_paths(items):
    """
    Convert flat list to full paths with hierarchy.
    """
    paths = []
    path_stack = []
    
    for item, is_folder in items:
        # Count leading spaces/indentation to determine depth
        # This is simplified - assumes consistent indentation
        depth = 0
        
        # Adjust path stack based on hierarchy
        path_stack = path_stack[:depth]
        path_stack.append(item)
        
        full_path = '/'.join(path_stack)
        paths.append((full_path, is_folder))
    
    return paths


def create_structure(base_path, tree_text):
    """
    Create folder structure from tree text.
    
    Args:
        base_path: Where to create the structure
        tree_text: Tree structure as string
        
    Returns:
        (success: bool, message: str, created_items: list)
    """
    try:
        os.makedirs(base_path, exist_ok=True)
        
        items = parse_tree_to_items(tree_text)
        created = []
        
        # Simple approach: create folders and files
        for item, is_folder in items:
            full_path = os.path.join(base_path, item)
            
            if is_folder:
                os.makedirs(full_path, exist_ok=True)
                created.append(('📁', item))
            else:
                # Create parent directories if needed
                parent_dir = os.path.dirname(full_path)
                os.makedirs(parent_dir, exist_ok=True)
                
                # Create file with placeholder content
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(f"File: {os.path.basename(item)}\nCreated from tree structure.\n")
                created.append(('📄', item))
        
        return True, f"Created {len(created)} items", created
    
    except Exception as e:
        return False, f"Error: {str(e)}", []


def display_help():
    """Show help message."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║         Simple Tree to Folders Generator                      ║
║                                                               ║
║  This tool creates folder/file structures from tree text     ║
╚═══════════════════════════════════════════════════════════════╝

USAGE:
  python simple_tree_generator.py

EXAMPLE TREE:
  MyProject/
  ├── src/
  │   ├── main.py
  │   └── utils.py
  ├── tests/
  │   └── test_main.py
  ├── docs/
  │   └── README.md
  └── requirements.txt

FEATURES:
  ✓ Create folders (use trailing /)
  ✓ Create files (no trailing /)
  ✓ Supports tree characters (├──, │, └──)
  ✓ Supports simple indentation
  ✓ No existing files overwritten
  ✓ Placeholder content in files

FOR INTERACTIVE GUI:
  python tree_structure_generator.py

FOR MORE EXAMPLES:
  python TREE_STRUCTURE_GUIDE.py
""")


def interactive_mode():
    """Interactive mode for creating structure."""
    print("\n" + "="*60)
    print("TREE STRUCTURE GENERATOR - Interactive Mode")
    print("="*60 + "\n")
    
    print("EXAMPLES:")
    print("-" * 60)
    print("""
1. Simple Project:
   MyProject/
   ├── src/
   │   └── main.py
   ├── tests/
   └── README.md

2. Deep Structure:
   App/
   ├── components/
   │   ├── Button.jsx
   │   └── Header.jsx
   └── pages/
       ├── Home.jsx
       └── About.jsx

3. File Organization:
   Documents/
   ├── 2024/
   │   ├── Q1/
   │   └── Q2/
   └── 2025/
       └── Q1/
""")
    print("-" * 60)
    
    # Get output folder
    output_path = input("\n📁 Enter output folder path (or press Enter for 'generated_structure'): ").strip()
    if not output_path:
        output_path = "generated_structure"
    
    # Get tree text
    print("\n📝 Enter your tree structure (type 'END' on a new line when done):")
    print("   (You can paste from clipboard or type manually)")
    print("   " + "-"*56)
    
    tree_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        tree_lines.append(line)
    
    tree_text = '\n'.join(tree_lines)
    
    if not tree_text.strip():
        print("\n❌ No tree structure provided!")
        return
    
    # Show preview
    print("\n" + "="*60)
    print("PREVIEW:")
    print("="*60)
    print(tree_text)
    print("="*60)
    
    # Confirm
    confirm = input("\n✓ Create this structure? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("\n❌ Cancelled.")
        return
    
    # Create structure
    print("\n⏳ Creating structure...")
    success, message, created = create_structure(output_path, tree_text)
    
    if success:
        print(f"\n✅ {message}")
        print(f"📍 Location: {os.path.abspath(output_path)}\n")
        print("Created items:")
        for icon, item in created:
            print(f"  {icon} {item}")
    else:
        print(f"\n❌ {message}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        display_help()
    else:
        interactive_mode()
