"""
ALL-IN-ONE Structure Generator
Unified interface for all structure generation methods
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os


class AllInOneGenerator:
    """Main launcher for all structure generation tools."""
    
    def __init__(self, root):
        """Initialize the launcher."""
        self.root = root
        self.root.title("All-in-One Structure Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="All-in-One Structure Generator", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        subtitle = ttk.Label(main_frame, text="Choose how you want to create your folder structure:",
                           font=("Arial", 10), foreground="gray")
        subtitle.pack(pady=(0, 30))
        
        # Tools frame
        tools_frame = ttk.Frame(main_frame)
        tools_frame.pack(fill="both", expand=True)
        
        # Tool 1: Simple Tree Generator
        self.create_tool_button(
            tools_frame,
            title="📝 Simple Tree Generator",
            description="Quickly create folders from tree text\n(Best for: Quick, simple structures)",
            command=lambda: self.launch_tool("simple_tree_generator.py"),
            row=0
        )
        
        # Tool 2: Tree Structure Generator (GUI)
        self.create_tool_button(
            tools_frame,
            title="🌳 Tree Structure GUI",
            description="Full-featured tree structure editor\n(Best for: Complex structures with preview)",
            command=lambda: self.launch_tool("tree_structure_generator.py"),
            row=1
        )
        
        # Tool 3: Excel to Structure
        self.create_tool_button(
            tools_frame,
            title="📊 Excel to Structure",
            description="Create folders from Excel data\n(Best for: Data-driven structures)",
            command=lambda: self.launch_tool("excel_to_structure_gui.py"),
            row=2
        )
        
        # Tool 4: Folder to Tree
        self.create_tool_button(
            tools_frame,
            title="📁 Folder to Tree Visualizer",
            description="Convert existing folders to tree diagram\n(Best for: Analyzing folder structures)",
            command=lambda: self.launch_tool("folder_to_tree_visualizer.py"),
            row=3
        )
        
        # Tool 5: Help
        self.create_tool_button(
            tools_frame,
            title="📚 View Guide & Examples",
            description="Read comprehensive guide and examples\n(Best for: Learning how to use)",
            command=lambda: self.launch_tool("TREE_STRUCTURE_GUIDE.py"),
            row=4
        )
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill="x", pady=(20, 0), side="bottom")
        
        ttk.Label(footer_frame, text="💡 Tip: Start with 'Simple Tree Generator' for quick tasks",
                 font=("Arial", 9), foreground="blue").pack()
    
    def create_tool_button(self, parent, title, description, command, row):
        """Create a tool button with description."""
        
        frame = ttk.Frame(parent, relief="solid", borderwidth=1)
        frame.pack(fill="x", pady=8)
        
        # Add hover effect
        def on_enter(e):
            frame.configure(relief="raised")
        
        def on_leave(e):
            frame.configure(relief="solid")
        
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        
        # Content frame
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(content_frame, text=title, font=("Arial", 11, "bold"))
        title_label.pack(anchor="w")
        
        # Description
        desc_label = ttk.Label(content_frame, text=description, font=("Arial", 9), 
                              foreground="gray", justify="left")
        desc_label.pack(anchor="w", pady=(5, 0))
        
        # Button
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        btn = ttk.Button(btn_frame, text="Launch →", command=command)
        btn.pack(side="right")
        
        # Make frame clickable
        frame.config(cursor="hand2")
        frame.bind("<Button-1>", lambda e: command())
        title_label.bind("<Button-1>", lambda e: command())
        desc_label.bind("<Button-1>", lambda e: command())
    
    def launch_tool(self, script_name):
        """Launch a tool script."""
        try:
            if script_name == "TREE_STRUCTURE_GUIDE.py":
                # Show guide in a text window
                result = subprocess.run([sys.executable, script_name], 
                                      capture_output=True, text=True)
                
                # Create new window to show guide
                guide_window = tk.Toplevel(self.root)
                guide_window.title("Tree Structure Guide")
                guide_window.geometry("800x600")
                
                from tkinter.scrolledtext import ScrolledText
                text_widget = ScrolledText(guide_window, wrap="word")
                text_widget.pack(fill="both", expand=True, padx=10, pady=10)
                text_widget.insert("1.0", result.stdout)
                text_widget.config(state="disabled")
                
            else:
                # Launch tool as subprocess
                subprocess.Popen([sys.executable, script_name])
                messagebox.showinfo("Launched", f"Started {script_name}\n\nThis window will close.")
                self.root.after(1000, self.root.quit)
        
        except FileNotFoundError:
            messagebox.showerror("Error", f"Could not find {script_name}\n\nMake sure you're in the correct directory.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch {script_name}:\n{str(e)}")


def main():
    """Main function."""
    root = tk.Tk()
    app = AllInOneGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
