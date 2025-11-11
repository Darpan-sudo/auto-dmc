"""
Excel File Upload & File Structure Generator with GUI
This script provides a graphical interface to upload Excel files,
edit data, and generate file/folder structures.
"""

import os
import json
import pandas as pd
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import threading


class ExcelStructureGUI:
    """GUI for Excel to File Structure conversion."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Excel to File Structure Generator")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Data storage
        self.excel_file = None
        self.dataframe = None
        self.output_path = None
        
        # Setup GUI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        
        # Main container with notebook (tabs)
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # Input file selection
        ttk.Label(header_frame, text="Input Excel File:").grid(row=0, column=0, sticky="w", padx=5)
        self.input_file_label = ttk.Label(header_frame, text="No file selected", foreground="gray")
        self.input_file_label.grid(row=0, column=1, sticky="w", padx=5)
        ttk.Button(header_frame, text="Browse Input", command=self.browse_input_file).grid(row=0, column=2, padx=5)
        
        # Output path selection
        ttk.Label(header_frame, text="Output Folder:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.output_path_label = ttk.Label(header_frame, text="No folder selected", foreground="gray")
        self.output_path_label.grid(row=1, column=1, sticky="w", padx=5)
        ttk.Button(header_frame, text="Browse Output", command=self.browse_output_folder).grid(row=1, column=2, padx=5)
        
        # Notebook (tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky="nsew", pady=10)
        main_frame.rowconfigure(1, weight=1)
        
        # Tab 1: Data Preview & Edit
        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text="Data Preview & Edit")
        self.setup_preview_tab(preview_frame)
        
        # Tab 2: Options
        options_frame = ttk.Frame(notebook)
        notebook.add(options_frame, text="Options")
        self.setup_options_tab(options_frame)
        
        # Tab 3: Output Log
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="Output Log")
        self.setup_log_tab(log_frame)
        
        # Footer with buttons
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=2, column=0, sticky="ew", pady=10)
        footer_frame.columnconfigure(0, weight=1)
        
        ttk.Button(footer_frame, text="Load Excel", command=self.load_excel_file).pack(side="left", padx=5)
        ttk.Button(footer_frame, text="Save Changes as CSV", command=self.save_changes_csv).pack(side="left", padx=5)
        ttk.Button(footer_frame, text="Generate Structure", command=self.generate_structure_threaded).pack(side="left", padx=5)
        ttk.Button(footer_frame, text="Export as JSON", command=self.export_json).pack(side="left", padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(footer_frame, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="left", fill="x", expand=True, padx=(10, 0))
    
    def setup_preview_tab(self, parent):
        """Setup the data preview and edit tab."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        # Treeview for data display and editing
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.tree = ttk.Treeview(tree_frame, yscroll=vsb.set, xscroll=hsb.set)
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Bind double-click for editing
        self.tree.bind("<Double-1>", self.edit_cell)
        
        # Info label
        info_label = ttk.Label(parent, text="Double-click cells to edit • Rows shown: 0", foreground="gray")
        info_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.info_label = info_label
    
    def setup_options_tab(self, parent):
        """Setup the options tab."""
        parent.columnconfigure(0, weight=1)
        
        # Structure type
        type_frame = ttk.LabelFrame(parent, text="Structure Type", padding="10")
        type_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        self.structure_type = tk.StringVar(value="folder_only")
        ttk.Radiobutton(type_frame, text="Folders Only (No Files)", variable=self.structure_type, 
                       value="folder_only").pack(anchor="w", pady=5)
        ttk.Radiobutton(type_frame, text="Folders + Text Files", variable=self.structure_type, 
                       value="folder_files").pack(anchor="w", pady=5)
        ttk.Radiobutton(type_frame, text="Custom (Last column as filename)", variable=self.structure_type, 
                       value="custom").pack(anchor="w", pady=5)
        
        # File extension
        ext_frame = ttk.LabelFrame(parent, text="File Options", padding="10")
        ext_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        ttk.Label(ext_frame, text="File Extension:").pack(anchor="w", pady=5)
        self.file_extension = ttk.Combobox(ext_frame, values=[".txt", ".md", ".json", ".csv", ".log"], state="readonly")
        self.file_extension.set(".txt")
        self.file_extension.pack(anchor="w", fill="x", pady=5)
        
        # Create readme
        self.create_readme = tk.BooleanVar(value=True)
        ttk.Checkbutton(ext_frame, text="Create README in each folder", variable=self.create_readme).pack(anchor="w", pady=5)
        
        # Empty folders only
        self.empty_folders = tk.BooleanVar(value=False)
        ttk.Checkbutton(ext_frame, text="Create empty folders (no files)", variable=self.empty_folders).pack(anchor="w", pady=5)
    
    def setup_log_tab(self, parent):
        """Setup the output log tab."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        self.log_text = ScrolledText(parent, wrap="word", height=20, width=80)
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Clear button
        ttk.Button(parent, text="Clear Log", command=lambda: self.log_text.delete("1.0", "end")).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    
    def log(self, message):
        """Add message to log."""
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.root.update()
    
    def browse_input_file(self):
        """Browse for input Excel file."""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel Files", "*.xlsx *.xls"), ("All Files", "*.*")]
        )
        if file_path:
            self.excel_file = file_path
            self.input_file_label.config(text=os.path.basename(file_path), foreground="black")
            self.status_var.set(f"Selected input: {os.path.basename(file_path)}")
    
    def browse_output_folder(self):
        """Browse for output folder."""
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_path = folder_path
            self.output_path_label.config(text=folder_path, foreground="black")
            self.status_var.set(f"Selected output: {folder_path}")
    
    def load_excel_file(self):
        """Load the selected Excel file."""
        if not self.excel_file:
            messagebox.showwarning("Warning", "Please select an Excel file first!")
            return
        
        try:
            self.dataframe = pd.read_excel(self.excel_file)
            self.display_data_in_tree()
            self.status_var.set(f"Loaded: {self.dataframe.shape[0]} rows, {self.dataframe.shape[1]} columns")
            messagebox.showinfo("Success", f"Excel file loaded!\n{self.dataframe.shape[0]} rows × {self.dataframe.shape[1]} columns")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Excel file:\n{str(e)}")
            self.status_var.set("Error loading file")
    
    def display_data_in_tree(self):
        """Display dataframe in treeview."""
        if self.dataframe is None:
            return
        
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Define columns
        columns = list(self.dataframe.columns)
        self.tree["columns"] = columns
        self.tree.column("#0", width=30, anchor="center")
        self.tree.heading("#0", text="Row")
        
        for col in columns:
            self.tree.column(col, width=100, anchor="w")
            self.tree.heading(col, text=col)
        
        # Insert data
        for idx, row in self.dataframe.iterrows():
            values = [str(row[col]) if pd.notna(row[col]) else "" for col in columns]
            self.tree.insert("", "end", text=str(idx), values=values)
        
        self.info_label.config(text=f"Rows shown: {len(self.dataframe)}")
    
    def edit_cell(self, event):
        """Allow cell editing on double-click."""
        item = self.tree.selection()[0]
        col = self.tree.identify_column(event.x)
        
        if col == "#0":
            return
        
        col_index = int(col) - 1
        row_index = self.tree.index(item)
        current_value = self.tree.item(item)["values"][col_index]
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Cell")
        edit_window.geometry("300x150")
        
        ttk.Label(edit_window, text=f"Edit Row {row_index}, Column {self.dataframe.columns[col_index]}:").pack(padx=10, pady=10)
        
        text_widget = tk.Text(edit_window, height=3, width=30)
        text_widget.pack(padx=10, pady=5, fill="both", expand=True)
        text_widget.insert("1.0", str(current_value))
        text_widget.focus()
        
        def save_edit():
            new_value = text_widget.get("1.0", "end").strip()
            self.dataframe.iloc[row_index, col_index] = new_value
            
            values = list(self.tree.item(item)["values"])
            values[col_index] = new_value
            self.tree.item(item, values=values)
            
            edit_window.destroy()
            self.status_var.set(f"Updated cell at Row {row_index}")
        
        ttk.Button(edit_window, text="Save", command=save_edit).pack(padx=10, pady=5)
    
    def save_changes_csv(self):
        """Save edited data as CSV."""
        if self.dataframe is None:
            messagebox.showwarning("Warning", "No data to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                self.dataframe.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Data saved to:\n{file_path}")
                self.log(f"✓ Data saved to CSV: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save CSV:\n{str(e)}")
    
    def export_json(self):
        """Export data as JSON."""
        if self.dataframe is None:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                data_dict = self.dataframe.to_dict("records")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data_dict, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", f"Data exported to:\n{file_path}")
                self.log(f"✓ Data exported to JSON: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export JSON:\n{str(e)}")
    
    def generate_structure_threaded(self):
        """Generate structure in a separate thread."""
        if self.dataframe is None:
            messagebox.showwarning("Warning", "Please load Excel file first!")
            return
        
        if not self.output_path:
            messagebox.showwarning("Warning", "Please select output folder!")
            return
        
        thread = threading.Thread(target=self.generate_structure)
        thread.start()
    
    def generate_structure(self):
        """Generate the file structure."""
        try:
            self.log("\n" + "="*60)
            self.log("Starting structure generation...")
            self.log(f"Output Path: {self.output_path}")
            self.log(f"Structure Type: {self.structure_type.get()}")
            self.log("="*60)
            
            os.makedirs(self.output_path, exist_ok=True)
            created_count = 0
            
            structure_type = self.structure_type.get()
            file_ext = self.file_extension.get() if not self.empty_folders.get() else ""
            
            for idx, row in self.dataframe.iterrows():
                current_path = self.output_path
                
                if structure_type == "folder_only" or self.empty_folders.get():
                    # Create folder hierarchy from all columns
                    for col in self.dataframe.columns:
                        value = str(row[col]).strip()
                        if value and value != "nan":
                            current_path = os.path.join(current_path, value)
                    
                    os.makedirs(current_path, exist_ok=True)
                    created_count += 1
                    self.log(f"✓ Folder: {os.path.relpath(current_path, self.output_path)}")
                    
                    # Create README if selected
                    if self.create_readme.get():
                        readme_path = os.path.join(current_path, "README.md")
                        if not os.path.exists(readme_path):
                            with open(readme_path, "w", encoding="utf-8") as f:
                                f.write(f"# {os.path.basename(current_path)}\n\nCreated from Excel structure.\n")
                
                else:
                    # Create folder structure with files
                    for col in self.dataframe.columns[:-1]:
                        value = str(row[col]).strip()
                        if value and value != "nan":
                            current_path = os.path.join(current_path, value)
                    
                    os.makedirs(current_path, exist_ok=True)
                    
                    # Create file from last column
                    last_col_value = str(row[self.dataframe.columns[-1]]).strip()
                    if last_col_value and last_col_value != "nan":
                        file_path = os.path.join(current_path, f"{last_col_value}{file_ext}")
                        if not os.path.exists(file_path):
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(f"File: {last_col_value}\nCreated from Excel structure.\n")
                            created_count += 1
                            self.log(f"✓ File: {os.path.relpath(file_path, self.output_path)}")
            
            self.log("="*60)
            self.log(f"✓ Structure generation complete!")
            self.log(f"  Total items created: {created_count}")
            self.log("="*60 + "\n")
            
            self.status_var.set(f"Success! Created {created_count} items")
            messagebox.showinfo("Success", f"Structure generated successfully!\n\nCreated {created_count} items in:\n{self.output_path}")
            
        except Exception as e:
            self.log(f"✗ Error: {str(e)}\n")
            messagebox.showerror("Error", f"Failed to generate structure:\n{str(e)}")
            self.status_var.set("Error generating structure")


def main():
    """Main function."""
    root = tk.Tk()
    app = ExcelStructureGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
