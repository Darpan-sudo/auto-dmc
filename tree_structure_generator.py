"""
Tree Structure Parser & File Generator
Converts tree structure (text format) into actual file/folder structure
Supports both ASCII and visual tree formats
"""

import os
import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import threading


class TreeStructureParser:
    """Parse and create file structures from tree representation."""
    
    def __init__(self):
        """Initialize the parser."""
        self.tree_lines = []
        self.structure = []
        
    def parse_tree(self, tree_text):
        """
        Parse tree structure from text.
        
        Supports formats like:
        Project/
        ├── src/
        │   ├── main.py
        │   └── utils.py
        ├── tests/
        │   └── test_main.py
        └── README.md
        
        Args:
            tree_text (str): Tree structure as text
            
        Returns:
            list: List of tuples (path, is_folder)
        """
        self.tree_lines = tree_text.strip().split('\n')
        self.structure = []
        
        for line in self.tree_lines:
            path = self._extract_path(line)
            if path:
                is_folder = path.endswith('/')
                if is_folder:
                    path = path[:-1]  # Remove trailing slash
                self.structure.append((path, is_folder))
        
        return self.structure
    
    def _extract_path(self, line):
        """
        Extract the actual path from a tree line.
        
        Removes tree characters like ├──, │, └──, etc.
        """
        # Remove all tree drawing characters
        tree_chars = ['├── ', '├─', '│   ', '│', '└── ', '└─', '   ', '  ']
        
        cleaned = line
        for char in tree_chars:
            cleaned = cleaned.replace(char, '')
        
        cleaned = cleaned.strip()
        
        if cleaned:
            return cleaned
        return None
    
    def build_hierarchical_structure(self):
        """
        Build hierarchical structure from flat list.
        
        Returns:
            dict: Hierarchical structure
        """
        hierarchy = {}
        
        for path, is_folder in self.structure:
            parts = path.split('/')
            current = hierarchy
            
            for i, part in enumerate(parts):
                if part not in current:
                    is_last = (i == len(parts) - 1)
                    current[part] = {
                        '_is_folder': is_folder or (i < len(parts) - 1),
                        '_children': {}
                    }
                current = current[part]['_children']
        
        return hierarchy
    
    def create_structure(self, base_path):
        """
        Create actual files and folders from structure.
        
        Args:
            base_path (str): Base path to create structure
            
        Returns:
            tuple: (created_count, created_items)
        """
        created_count = 0
        created_items = []
        
        def process_dict(d, current_path):
            nonlocal created_count
            
            for key, value in d.items():
                if key.startswith('_'):
                    continue
                
                item_path = os.path.join(current_path, key)
                
                if value['_is_folder']:
                    os.makedirs(item_path, exist_ok=True)
                    created_count += 1
                    created_items.append(('folder', os.path.relpath(item_path, base_path)))
                else:
                    os.makedirs(os.path.dirname(item_path), exist_ok=True)
                    with open(item_path, 'w', encoding='utf-8') as f:
                        f.write(f"File: {key}\nCreated from tree structure.\n")
                    created_count += 1
                    created_items.append(('file', os.path.relpath(item_path, base_path)))
                
                # Process children
                if value['_children']:
                    process_dict(value['_children'], item_path)
        
        os.makedirs(base_path, exist_ok=True)
        hierarchy = self.build_hierarchical_structure()
        process_dict(hierarchy, base_path)
        
        return created_count, created_items


class TreeStructureGUI:
    """GUI for Tree Structure to Files conversion."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Tree Structure to Files Generator")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Data storage
        self.tree_text = None
        self.output_path = None
        self.parser = TreeStructureParser()
        
        # Setup GUI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # Output path
        ttk.Label(header_frame, text="Output Folder:").grid(row=0, column=0, sticky="w", padx=5)
        self.output_path_label = ttk.Label(header_frame, text="No folder selected", foreground="gray")
        self.output_path_label.grid(row=0, column=1, sticky="w", padx=5)
        ttk.Button(header_frame, text="Browse Output", command=self.browse_output_folder).grid(row=0, column=2, padx=5)
        
        # Notebook (tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky="nsew", pady=10)
        main_frame.rowconfigure(1, weight=1)
        
        # Tab 1: Tree Input
        input_frame = ttk.Frame(notebook)
        notebook.add(input_frame, text="Tree Structure Input")
        self.setup_input_tab(input_frame)
        
        # Tab 2: Preview
        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text="Structure Preview")
        self.setup_preview_tab(preview_frame)
        
        # Tab 3: Output Log
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="Output Log")
        self.setup_log_tab(log_frame)
        
        # Footer with buttons
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=2, column=0, sticky="ew", pady=10)
        footer_frame.columnconfigure(0, weight=1)
        
        ttk.Button(footer_frame, text="Load from File", command=self.load_from_file).pack(side="left", padx=5)
        ttk.Button(footer_frame, text="Parse Tree", command=self.parse_tree).pack(side="left", padx=5)
        ttk.Button(footer_frame, text="Generate Structure", command=self.generate_structure_threaded).pack(side="left", padx=5)
        ttk.Button(footer_frame, text="Save Tree as Text", command=self.save_tree_text).pack(side="left", padx=5)
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(footer_frame, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="left", fill="x", expand=True, padx=(10, 0))
    
    def setup_input_tab(self, parent):
        """Setup the tree input tab."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        
        # Instructions
        instructions = ttk.Label(parent, text="Paste your tree structure here. Use ├──, │, └── for tree characters (or just use simple indentation).\nExample formats shown below.", wraplength=1000, justify="left")
        instructions.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Text area
        self.tree_input = ScrolledText(parent, wrap="word", height=30, width=100)
        self.tree_input.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Sample buttons
        sample_frame = ttk.Frame(parent)
        sample_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        ttk.Button(sample_frame, text="Load Sample 1: Simple Project", 
                  command=lambda: self.load_sample(1)).pack(side="left", padx=5)
        ttk.Button(sample_frame, text="Load Sample 2: Deep Structure", 
                  command=lambda: self.load_sample(2)).pack(side="left", padx=5)
        ttk.Button(sample_frame, text="Load Sample 3: Document Structure", 
                  command=lambda: self.load_sample(3)).pack(side="left", padx=5)
    
    def setup_preview_tab(self, parent):
        """Setup the preview tab."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        ttk.Label(parent, text="Parsed Structure Preview:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        
        self.preview_text = ScrolledText(parent, wrap="word", height=30, width=100)
        self.preview_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    
    def setup_log_tab(self, parent):
        """Setup the output log tab."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        self.log_text = ScrolledText(parent, wrap="word", height=30, width=100)
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        ttk.Button(parent, text="Clear Log", command=lambda: self.log_text.delete("1.0", "end")).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    
    def log(self, message):
        """Add message to log."""
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.root.update()
    
    def browse_output_folder(self):
        """Browse for output folder."""
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_path = folder_path
            self.output_path_label.config(text=folder_path, foreground="black")
            self.status_var.set(f"Output: {folder_path}")
    
    def load_sample(self, sample_num):
        """Load a sample tree structure."""
        samples = {
            1: """MyProject/
├── src/
│   ├── main.py
│   ├── utils.py
│   └── config.py
├── tests/
│   ├── test_main.py
│   └── test_utils.py
├── docs/
│   └── README.md
└── requirements.txt""",
            
            2: """Company/
├── Engineering/
│   ├── Backend/
│   │   ├── api/
│   │   │   ├── routes.py
│   │   │   └── handlers.py
│   │   ├── database/
│   │   │   └── models.py
│   │   └── tests/
│   │       └── test_api.py
│   └── Frontend/
│       ├── components/
│       │   ├── Button.jsx
│       │   └── Header.jsx
│       └── pages/
│           ├── Home.jsx
│           └── About.jsx
├── Sales/
│   ├── 2024/
│   │   ├── Q1/
│   │   │   └── report.xlsx
│   │   └── Q2/
│   │       └── report.xlsx
│   └── 2025/
│       └── Q1/
│           └── report.xlsx
└── HR/
    ├── Policies/
    │   └── handbook.pdf
    └── Training/
        └── onboarding.pdf""",
            
            3: """DocumentArchive/
├── 2024/
│   ├── January/
│   │   ├── invoices/
│   │   │   ├── INV001.pdf
│   │   │   └── INV002.pdf
│   │   ├── contracts/
│   │   │   └── contract_001.pdf
│   │   └── reports/
│   │       └── monthly_report.pdf
│   ├── February/
│   │   ├── invoices/
│   │   │   └── INV003.pdf
│   │   └── reports/
│   │       └── monthly_report.pdf
│   └── March/
│       └── invoices/
│           └── INV004.pdf
└── 2025/
    └── January/
        ├── invoices/
        └── reports/"""
        }
        
        self.tree_input.delete("1.0", "end")
        self.tree_input.insert("1.0", samples.get(sample_num, ""))
        self.status_var.set(f"Loaded Sample {sample_num}")
    
    def load_from_file(self):
        """Load tree structure from a text file."""
        file_path = filedialog.askopenfilename(
            title="Select Tree Structure File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.tree_input.delete("1.0", "end")
                self.tree_input.insert("1.0", content)
                self.status_var.set(f"Loaded from: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    
    def parse_tree(self):
        """Parse the tree structure from input."""
        tree_text = self.tree_input.get("1.0", "end").strip()
        
        if not tree_text:
            messagebox.showwarning("Warning", "Please enter tree structure first!")
            return
        
        try:
            structure = self.parser.parse_tree(tree_text)
            
            # Display preview
            preview = "Parsed Structure:\n" + "="*60 + "\n\n"
            
            for i, (path, is_folder) in enumerate(structure, 1):
                item_type = "📁 FOLDER" if is_folder else "📄 FILE"
                preview += f"{i}. {item_type}: {path}\n"
            
            preview += f"\n{'='*60}\n"
            preview += f"Total items: {len(structure)}\n"
            preview += f"Folders: {sum(1 for _, is_f in structure if is_f)}\n"
            preview += f"Files: {sum(1 for _, is_f in structure if not is_f)}\n"
            
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("1.0", preview)
            
            self.status_var.set(f"Parsed {len(structure)} items successfully")
            messagebox.showinfo("Success", f"Parsed {len(structure)} items!\n\nFolders: {sum(1 for _, is_f in structure if is_f)}\nFiles: {sum(1 for _, is_f in structure if not is_f)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse tree:\n{str(e)}")
            self.status_var.set("Error parsing tree")
    
    def generate_structure_threaded(self):
        """Generate structure in a separate thread."""
        tree_text = self.tree_input.get("1.0", "end").strip()
        
        if not tree_text:
            messagebox.showwarning("Warning", "Please enter tree structure first!")
            return
        
        if not self.output_path:
            messagebox.showwarning("Warning", "Please select output folder!")
            return
        
        thread = threading.Thread(target=self.generate_structure)
        thread.start()
    
    def generate_structure(self):
        """Generate the file structure."""
        try:
            tree_text = self.tree_input.get("1.0", "end").strip()
            
            self.log("\n" + "="*70)
            self.log("Starting structure generation from tree...")
            self.log(f"Output Path: {self.output_path}")
            self.log("="*70)
            
            # Parse tree
            self.parser.parse_tree(tree_text)
            
            # Create structure
            created_count, created_items = self.parser.create_structure(self.output_path)
            
            # Log results
            self.log(f"\nCreated {created_count} items:\n")
            for item_type, path in created_items:
                icon = "📁" if item_type == "folder" else "📄"
                self.log(f"{icon} {path}")
            
            self.log("\n" + "="*70)
            self.log(f"✓ Structure generation complete!")
            self.log(f"  Total items created: {created_count}")
            self.log("="*70 + "\n")
            
            self.status_var.set(f"Success! Created {created_count} items")
            messagebox.showinfo("Success", f"Structure generated successfully!\n\nCreated {created_count} items in:\n{self.output_path}")
            
        except Exception as e:
            error_msg = f"✗ Error: {str(e)}\n"
            self.log(error_msg)
            messagebox.showerror("Error", f"Failed to generate structure:\n{str(e)}")
            self.status_var.set("Error generating structure")
    
    def save_tree_text(self):
        """Save tree structure to a text file."""
        tree_text = self.tree_input.get("1.0", "end").strip()
        
        if not tree_text:
            messagebox.showwarning("Warning", "Please enter tree structure first!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(tree_text)
                messagebox.showinfo("Success", f"Tree structure saved to:\n{file_path}")
                self.log(f"✓ Tree structure saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{str(e)}")


def main():
    """Main function."""
    root = tk.Tk()
    app = TreeStructureGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
