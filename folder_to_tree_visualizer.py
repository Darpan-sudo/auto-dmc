"""
Folder to Tree Structure Visualizer
Convert existing folder structures into beautiful tree diagrams
"""

import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import threading


class FolderToTree:
    """Convert folder structure to tree visualization."""
    
    def __init__(self):
        """Initialize the converter."""
        self.tree_output = ""
        
    def scan_folder(self, folder_path, prefix="", is_last=True, max_depth=None, current_depth=0, ignore_patterns=None):
        """
        Scan folder and generate tree structure.
        
        Args:
            folder_path (str): Path to scan
            prefix (str): Prefix for tree characters
            is_last (bool): Is this the last item
            max_depth (int): Maximum depth to scan
            current_depth (int): Current depth level
            ignore_patterns (list): Patterns to ignore
            
        Returns:
            str: Tree representation
        """
        if ignore_patterns is None:
            ignore_patterns = ['.git', '__pycache__', '.pyc', 'node_modules', '.env']
        
        if max_depth and current_depth >= max_depth:
            return ""
        
        output = ""
        
        try:
            items = sorted(os.listdir(folder_path))
        except PermissionError:
            return f"{prefix}[Permission Denied]\n"
        
        # Filter items
        filtered_items = []
        for item in items:
            should_ignore = False
            for pattern in ignore_patterns:
                if pattern in item:
                    should_ignore = True
                    break
            if not should_ignore:
                filtered_items.append(item)
        
        for i, item in enumerate(filtered_items):
            item_path = os.path.join(folder_path, item)
            is_last_item = (i == len(filtered_items) - 1)
            
            # Determine connector
            connector = "└── " if is_last_item else "├── "
            extension = "    " if is_last_item else "│   "
            
            # Add item to output
            if os.path.isdir(item_path):
                output += f"{prefix}{connector}{item}/\n"
                # Recursively process subdirectories
                new_prefix = prefix + extension
                output += self.scan_folder(item_path, new_prefix, is_last_item, max_depth, 
                                          current_depth + 1, ignore_patterns)
            else:
                output += f"{prefix}{connector}{item}\n"
        
        return output
    
    def generate_tree(self, folder_path, max_depth=None, ignore_patterns=None):
        """
        Generate tree from folder.
        
        Args:
            folder_path (str): Root folder path
            max_depth (int): Max depth to scan
            ignore_patterns (list): Patterns to ignore
            
        Returns:
            str: Tree representation
        """
        if not os.path.exists(folder_path):
            return f"Error: Folder not found: {folder_path}"
        
        folder_name = os.path.basename(folder_path)
        tree = f"{folder_name}/\n"
        tree += self.scan_folder(folder_path, "", True, max_depth, 0, ignore_patterns)
        
        return tree
    
    def count_items(self, tree_text):
        """
        Count files and folders in tree.
        
        Args:
            tree_text (str): Tree representation
            
        Returns:
            dict: Count statistics
        """
        lines = tree_text.strip().split('\n')
        folders = sum(1 for line in lines if line.rstrip().endswith('/'))
        files = sum(1 for line in lines if not line.rstrip().endswith('/') and line.strip())
        
        return {
            'total': len(lines),
            'folders': folders,
            'files': files
        }


class TreeVisualizerGUI:
    """GUI for converting folders to tree structures."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Folder to Tree Structure Visualizer")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Data storage
        self.folder_path = None
        self.converter = FolderToTree()
        
        # Setup GUI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Header - Folder Selection
        header_frame = ttk.LabelFrame(main_frame, text="Folder Selection", padding="10")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        ttk.Label(header_frame, text="Source Folder:").grid(row=0, column=0, sticky="w", padx=5)
        self.folder_label = ttk.Label(header_frame, text="No folder selected", foreground="gray")
        self.folder_label.grid(row=0, column=1, sticky="w", padx=5)
        ttk.Button(header_frame, text="Browse Folder", command=self.browse_folder).grid(row=0, column=2, padx=5)
        
        # Options Frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # Max Depth
        ttk.Label(options_frame, text="Max Depth:").grid(row=0, column=0, sticky="w", padx=5)
        self.max_depth_var = tk.StringVar(value="10")
        depth_spin = ttk.Spinbox(options_frame, from_=1, to=20, textvariable=self.max_depth_var, width=5)
        depth_spin.grid(row=0, column=1, sticky="w", padx=5)
        
        # Ignore patterns
        ttk.Label(options_frame, text="Ignore Patterns (comma-separated):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.ignore_patterns_var = tk.StringVar(value=".git,__pycache__,.pyc,node_modules,.env,.vscode")
        ignore_entry = ttk.Entry(options_frame, textvariable=self.ignore_patterns_var, width=60)
        ignore_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Statistics checkbox
        self.show_stats = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Show statistics", variable=self.show_stats).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        # Include hidden files
        self.include_hidden = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Include hidden files (.* files)", variable=self.include_hidden).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Notebook (tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=2, column=0, sticky="nsew", pady=10)
        main_frame.rowconfigure(2, weight=1)
        
        # Tab 1: Tree Preview
        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text="Tree Preview")
        self.setup_preview_tab(preview_frame)
        
        # Tab 2: Compact View
        compact_frame = ttk.Frame(notebook)
        notebook.add(compact_frame, text="Compact View")
        self.setup_compact_tab(compact_frame)
        
        # Tab 3: Statistics
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Statistics & Analysis")
        self.setup_stats_tab(stats_frame)
        
        # Footer with buttons
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=3, column=0, sticky="ew", pady=10)
        footer_frame.columnconfigure(0, weight=1)
        
        ttk.Button(footer_frame, text="Generate Tree", command=self.generate_tree_threaded).pack(side="left", padx=5)
        ttk.Button(footer_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(side="left", padx=5)
        ttk.Button(footer_frame, text="Save as Text File", command=self.save_as_file).pack(side="left", padx=5)
        ttk.Button(footer_frame, text="Save as Markdown", command=self.save_as_markdown).pack(side="left", padx=5)
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(footer_frame, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="left", fill="x", expand=True, padx=(10, 0))
    
    def setup_preview_tab(self, parent):
        """Setup the tree preview tab."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        self.tree_preview = ScrolledText(parent, wrap="word", height=30, width=100, font=("Courier", 9))
        self.tree_preview.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def setup_compact_tab(self, parent):
        """Setup the compact view tab."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        ttk.Label(parent, text="Compact tree (folders only):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        
        self.compact_view = ScrolledText(parent, wrap="word", height=30, width=100, font=("Courier", 9))
        self.compact_view.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    
    def setup_stats_tab(self, parent):
        """Setup the statistics tab."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        self.stats_text = ScrolledText(parent, wrap="word", height=30, width=100)
        self.stats_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def browse_folder(self):
        """Browse for a folder."""
        folder_path = filedialog.askdirectory(title="Select Folder to Convert")
        if folder_path:
            self.folder_path = folder_path
            self.folder_label.config(text=folder_path, foreground="black")
            self.status_var.set(f"Selected: {folder_path}")
    
    def generate_tree_threaded(self):
        """Generate tree in a separate thread."""
        if not self.folder_path:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return
        
        thread = threading.Thread(target=self.generate_tree)
        thread.start()
    
    def generate_tree(self):
        """Generate the tree structure."""
        try:
            self.status_var.set("Generating tree structure...")
            self.root.update()
            
            # Parse options
            max_depth = int(self.max_depth_var.get())
            ignore_patterns = [p.strip() for p in self.ignore_patterns_var.get().split(',')]
            
            # Generate tree
            tree = self.converter.generate_tree(self.folder_path, max_depth, ignore_patterns)
            
            # Display in preview
            self.tree_preview.delete("1.0", "end")
            self.tree_preview.insert("1.0", tree)
            
            # Generate compact view (folders only)
            compact_tree = self._generate_compact_tree(self.folder_path, "", True, max_depth, 0, ignore_patterns)
            self.compact_view.delete("1.0", "end")
            self.compact_view.insert("1.0", f"{os.path.basename(self.folder_path)}/\n{compact_tree}")
            
            # Generate statistics
            stats = self.converter.count_items(tree)
            self._display_statistics(stats, self.folder_path)
            
            self.status_var.set(f"✓ Generated tree: {stats['folders']} folders, {stats['files']} files")
            messagebox.showinfo("Success", f"Tree generated successfully!\n\nFolders: {stats['folders']}\nFiles: {stats['files']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate tree:\n{str(e)}")
            self.status_var.set("Error generating tree")
    
    def _generate_compact_tree(self, folder_path, prefix="", is_last=True, max_depth=None, 
                               current_depth=0, ignore_patterns=None):
        """Generate tree with folders only."""
        if ignore_patterns is None:
            ignore_patterns = []
        
        if max_depth and current_depth >= max_depth:
            return ""
        
        output = ""
        
        try:
            items = sorted([item for item in os.listdir(folder_path) 
                           if os.path.isdir(os.path.join(folder_path, item))])
        except PermissionError:
            return ""
        
        # Filter items
        filtered_items = []
        for item in items:
            should_ignore = False
            for pattern in ignore_patterns:
                if pattern in item:
                    should_ignore = True
                    break
            if not should_ignore:
                filtered_items.append(item)
        
        for i, item in enumerate(filtered_items):
            item_path = os.path.join(folder_path, item)
            is_last_item = (i == len(filtered_items) - 1)
            
            connector = "└── " if is_last_item else "├── "
            extension = "    " if is_last_item else "│   "
            
            output += f"{prefix}{connector}{item}/\n"
            new_prefix = prefix + extension
            output += self._generate_compact_tree(item_path, new_prefix, is_last_item, 
                                                  max_depth, current_depth + 1, ignore_patterns)
        
        return output
    
    def _display_statistics(self, stats, folder_path):
        """Display statistics."""
        stats_text = f"📊 FOLDER STRUCTURE STATISTICS\n"
        stats_text += "=" * 70 + "\n\n"
        stats_text += f"Source: {folder_path}\n"
        stats_text += f"Total Items: {stats['total']}\n"
        stats_text += f"Folders: {stats['folders']}\n"
        stats_text += f"Files: {stats['files']}\n\n"
        
        # File type analysis
        file_types = self._analyze_file_types(self.folder_path)
        if file_types:
            stats_text += "File Types Breakdown:\n"
            stats_text += "-" * 70 + "\n"
            for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
                stats_text += f"  {ext if ext else '[no extension]'}: {count}\n"
        
        self.stats_text.delete("1.0", "end")
        self.stats_text.insert("1.0", stats_text)
    
    def _analyze_file_types(self, folder_path):
        """Analyze file types in folder."""
        file_types = {}
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                ext = os.path.splitext(file)[1] or "[no extension]"
                file_types[ext] = file_types.get(ext, 0) + 1
        
        return file_types
    
    def copy_to_clipboard(self):
        """Copy tree to clipboard."""
        tree_text = self.tree_preview.get("1.0", "end")
        if not tree_text.strip():
            messagebox.showwarning("Warning", "No tree to copy!")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(tree_text)
        messagebox.showinfo("Success", "Tree copied to clipboard!")
        self.status_var.set("Copied to clipboard")
    
    def save_as_file(self):
        """Save tree as text file."""
        tree_text = self.tree_preview.get("1.0", "end")
        if not tree_text.strip():
            messagebox.showwarning("Warning", "No tree to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(tree_text)
                messagebox.showinfo("Success", f"Tree saved to:\n{file_path}")
                self.status_var.set(f"Saved to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{str(e)}")
    
    def save_as_markdown(self):
        """Save tree as markdown file."""
        tree_text = self.tree_preview.get("1.0", "end")
        if not tree_text.strip():
            messagebox.showwarning("Warning", "No tree to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                md_content = f"# Folder Structure\n\n```\n{tree_text}\n```\n"
                
                # Add statistics
                stats = self.converter.count_items(tree_text)
                md_content += f"\n## Summary\n"
                md_content += f"- **Total Items**: {stats['total']}\n"
                md_content += f"- **Folders**: {stats['folders']}\n"
                md_content += f"- **Files**: {stats['files']}\n"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                messagebox.showinfo("Success", f"Tree saved to:\n{file_path}")
                self.status_var.set(f"Saved to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{str(e)}")


def main():
    """Main function."""
    root = tk.Tk()
    app = TreeVisualizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
