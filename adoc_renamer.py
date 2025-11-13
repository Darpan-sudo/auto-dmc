"""
Adoc File Renaming Tool
Rename .adoc files based on their folder hierarchy
Example: project/subfolder/100.adoc -> project-subfolder-100.adoc
"""

import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import threading


class AdocRenamer:
    """Handle .adoc file renaming with hierarchy."""
    
    @staticmethod
    def get_folder_hierarchy(file_path, base_folder):
        """
        Get the folder hierarchy for a file.
        
        Example: 
          base: /root/project
          file: /root/project/docs/chapter1/100.adoc
          result: docs-chapter1-100
        
        Args:
            file_path (str): Full path to the file
            base_folder (str): Base folder path
            
        Returns:
            str: Hierarchical name without extension
        """
        path_obj = Path(file_path)
        base_obj = Path(base_folder)
        filename_without_ext = path_obj.stem
        
        # Get relative path from base folder
        relative_path = path_obj.relative_to(base_obj)
        
        # Get all parent directories (excluding filename)
        parts = list(relative_path.parts[:-1])  # Exclude the file itself
        
        # Add filename
        parts.append(filename_without_ext)
        
        # Join with hyphen
        return '-'.join(parts) if parts else filename_without_ext
    
    @staticmethod
    def rename_adoc_files(source_folder, dry_run=False, rename_in_place=False):
        """
        Rename all .adoc files with hierarchy.
        
        Args:
            source_folder (str): Folder to search for .adoc files
            dry_run (bool): Show what would be renamed without doing it
            rename_in_place (bool): Rename in place, else move to root with new name
            
        Returns:
            tuple: (total_renamed, details)
        """
        renamed_count = 0
        details = []
        
        # Find all .adoc files
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                if file.endswith('.adoc'):
                    old_path = os.path.join(root, file)
                    
                    # Generate new hierarchical name
                    hierarchy_name = AdocRenamer.get_folder_hierarchy(old_path, source_folder)
                    new_filename = f"{hierarchy_name}.adoc"
                    
                    if rename_in_place:
                        # Keep in same folder
                        new_path = os.path.join(root, new_filename)
                    else:
                        # Move to source_folder root
                        new_path = os.path.join(source_folder, new_filename)
                    
                    details.append({
                        'old_path': old_path,
                        'new_path': new_path,
                        'old_name': file,
                        'new_name': new_filename,
                        'old_relative': os.path.relpath(old_path, source_folder),
                        'new_relative': os.path.relpath(new_path, source_folder),
                    })
                    
                    if not dry_run:
                        try:
                            if os.path.exists(new_path):
                                # File already exists, skip
                                details[-1]['status'] = 'SKIPPED (already exists)'
                            else:
                                shutil.move(old_path, new_path)
                                details[-1]['status'] = 'RENAMED'
                                renamed_count += 1
                        except Exception as e:
                            details[-1]['status'] = f'ERROR: {str(e)}'
                    else:
                        details[-1]['status'] = 'PREVIEW'
                        renamed_count += 1
        
        return renamed_count, details


class AdocRenamerGUI:
    """GUI for Adoc file renaming."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Adoc File Renamer - Hierarchical Naming")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Data storage
        self.adoc_folder = None
        self.renamer = AdocRenamer()
        
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
        
        ttk.Label(header_frame, text="Adoc Folder:").grid(row=0, column=0, sticky="w", padx=5)
        self.folder_label = ttk.Label(header_frame, text="No folder selected", foreground="gray")
        self.folder_label.grid(row=0, column=1, sticky="w", padx=5)
        ttk.Button(header_frame, text="Browse Folder", command=self.browse_folder).grid(row=0, column=2, padx=5)
        
        # Info Frame
        info_frame = ttk.LabelFrame(main_frame, text="Information", padding="10")
        info_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        info_frame.columnconfigure(0, weight=1)
        
        info_text = """How it works:
• Select a folder containing .adoc files in subfolders
• The tool scans all subfolders for .adoc files
• Each file is renamed based on its folder hierarchy
• Example: documents/chapter1/section1/100.adoc → documents-chapter1-section1-100.adoc

Options:
□ Dry Run: Preview changes without actually renaming (default: checked)
□ Rename in Place: Keep files in their current folders (only change filename)
  (default: unchecked - moves to root folder with hierarchical name)"""
        
        ttk.Label(info_frame, text=info_text, justify="left").pack(anchor="w")
        
        # Options Frame
        options_frame = ttk.LabelFrame(main_frame, text="Renaming Options", padding="10")
        options_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        options_frame.columnconfigure(0, weight=1)
        options_frame.rowconfigure(1, weight=1)
        
        # Checkboxes
        checkbox_frame = ttk.Frame(options_frame)
        checkbox_frame.pack(anchor="w", pady=(0, 10))
        
        self.dry_run = tk.BooleanVar(value=True)
        ttk.Checkbutton(checkbox_frame, text="✓ Dry Run (Preview only - no changes made)", 
                       variable=self.dry_run).pack(anchor="w", pady=5)
        
        self.rename_in_place = tk.BooleanVar(value=False)
        ttk.Checkbutton(checkbox_frame, text="Rename in place (keep files in current folders)", 
                       variable=self.rename_in_place).pack(anchor="w", pady=5)
        
        # Preview/Results Text
        ttk.Label(options_frame, text="Preview / Results:", font=("Arial", 10, "bold")).pack(anchor="nw", pady=(10, 5))
        
        self.preview_text = ScrolledText(options_frame, wrap="word", height=20, width=140)
        self.preview_text.pack(fill="both", expand=True)
        
        # Footer with buttons
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=3, column=0, sticky="ew", pady=10)
        footer_frame.columnconfigure(0, weight=1)
        
        ttk.Button(footer_frame, text="Preview Changes", command=self.preview_rename_threaded).pack(side="left", padx=5)
        ttk.Button(footer_frame, text="Apply Changes", command=self.apply_rename_threaded).pack(side="left", padx=5)
        ttk.Button(footer_frame, text="Copy Preview to Clipboard", command=self.copy_to_clipboard).pack(side="left", padx=5)
        ttk.Button(footer_frame, text="Clear", command=lambda: self.preview_text.delete("1.0", "end")).pack(side="left", padx=5)
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(footer_frame, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="left", fill="x", expand=True, padx=(10, 0))
    
    def browse_folder(self):
        """Browse for a folder."""
        folder_path = filedialog.askdirectory(title="Select Folder with .adoc Files")
        if folder_path:
            self.adoc_folder = folder_path
            self.folder_label.config(text=folder_path, foreground="black")
            self.status_var.set(f"Selected: {folder_path}")
    
    def preview_rename_threaded(self):
        """Preview in separate thread."""
        if not self.adoc_folder:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return
        
        thread = threading.Thread(target=self.preview_rename)
        thread.start()
    
    def apply_rename_threaded(self):
        """Apply changes in separate thread."""
        if not self.adoc_folder:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to rename the files?\nThis action cannot be undone!"):
            thread = threading.Thread(target=self.apply_rename)
            thread.start()
    
    def preview_rename(self):
        """Preview the renaming."""
        try:
            self.preview_text.delete("1.0", "end")
            
            self.preview_text.insert("end", "="*100 + "\n")
            self.preview_text.insert("end", "PREVIEW: Adoc File Renaming\n")
            self.preview_text.insert("end", f"Folder: {self.adoc_folder}\n")
            self.preview_text.insert("end", f"Rename in place: {self.rename_in_place.get()}\n")
            self.preview_text.insert("end", "="*100 + "\n\n")
            self.root.update()
            
            # Get rename details
            renamed_count, details = self.renamer.rename_adoc_files(
                self.adoc_folder,
                dry_run=True,
                rename_in_place=self.rename_in_place.get()
            )
            
            if renamed_count == 0:
                self.preview_text.insert("end", "✗ No .adoc files found in the folder.\n")
            else:
                self.preview_text.insert("end", f"Found {renamed_count} .adoc file(s):\n\n")
                
                for i, detail in enumerate(details, 1):
                    self.preview_text.insert("end", f"{i}. Original: {detail['old_relative']}\n")
                    self.preview_text.insert("end", f"   Renamed:  {detail['new_relative']}\n")
                    self.preview_text.insert("end", "\n")
            
            self.preview_text.insert("end", "="*100 + "\n")
            self.preview_text.insert("end", f"Total files: {renamed_count}\n")
            self.preview_text.insert("end", "="*100 + "\n")
            self.preview_text.see("end")
            
            self.status_var.set(f"Preview complete - {renamed_count} files found")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview:\n{str(e)}")
            self.status_var.set("Error during preview")
    
    def apply_rename(self):
        """Apply the renaming."""
        try:
            self.preview_text.delete("1.0", "end")
            
            self.preview_text.insert("end", "="*100 + "\n")
            self.preview_text.insert("end", "APPLYING: Adoc File Renaming\n")
            self.preview_text.insert("end", f"Folder: {self.adoc_folder}\n")
            self.preview_text.insert("end", f"Rename in place: {self.rename_in_place.get()}\n")
            self.preview_text.insert("end", "="*100 + "\n\n")
            self.root.update()
            
            # Apply renaming
            renamed_count, details = self.renamer.rename_adoc_files(
                self.adoc_folder,
                dry_run=False,
                rename_in_place=self.rename_in_place.get()
            )
            
            success_count = 0
            for i, detail in enumerate(details, 1):
                status = detail.get('status', 'UNKNOWN')
                icon = "✓" if status == "RENAMED" else "⊘" if status == "SKIPPED" else "✗"
                
                self.preview_text.insert("end", f"{i}. {icon} {status}\n")
                self.preview_text.insert("end", f"   Original: {detail['old_relative']}\n")
                self.preview_text.insert("end", f"   New:      {detail['new_relative']}\n")
                
                if status == "RENAMED":
                    success_count += 1
                
                self.preview_text.insert("end", "\n")
            
            self.preview_text.insert("end", "="*100 + "\n")
            self.preview_text.insert("end", f"Successfully renamed: {success_count}/{len(details)} files\n")
            self.preview_text.insert("end", "="*100 + "\n")
            self.preview_text.see("end")
            
            self.status_var.set(f"✓ Complete - {success_count} files renamed")
            messagebox.showinfo("Success", f"Successfully renamed {success_count} file(s)!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply changes:\n{str(e)}")
            self.status_var.set("Error during renaming")
    
    def copy_to_clipboard(self):
        """Copy preview to clipboard."""
        text = self.preview_text.get("1.0", "end")
        if not text.strip():
            messagebox.showwarning("Warning", "No preview to copy!")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Success", "Preview copied to clipboard!")


def main():
    """Main function."""
    root = tk.Tk()
    app = AdocRenamerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
