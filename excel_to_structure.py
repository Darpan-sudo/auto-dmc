"""
Excel File Upload & File Structure Generator
This script allows you to upload an Excel file and generate a file/folder structure based on it.
"""

import os
import json
import pandas as pd
from pathlib import Path


class ExcelToStructure:
    """Converts Excel data into file and folder structures."""
    
    def __init__(self):
        """Initialize the structure generator."""
        self.excel_file = None
        self.dataframe = None
        self.output_base = None
        
    def load_excel(self, filepath):
        """
        Load an Excel file.
        
        Args:
            filepath (str): Path to the Excel file (.xlsx, .xls)
            
        Returns:
            pd.DataFrame: The loaded Excel data
        """
        try:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"File not found: {filepath}")
            
            # Load the Excel file
            self.excel_file = filepath
            self.dataframe = pd.read_excel(filepath)
            
            print(f"✓ Successfully loaded Excel file: {filepath}")
            print(f"  Dimensions: {self.dataframe.shape[0]} rows × {self.dataframe.shape[1]} columns")
            print(f"  Columns: {list(self.dataframe.columns)}\n")
            
            return self.dataframe
            
        except FileNotFoundError as e:
            print(f"✗ Error: {e}")
            return None
        except Exception as e:
            print(f"✗ Error loading Excel file: {e}")
            return None
    
    def display_preview(self, rows=5):
        """
        Display a preview of the loaded data.
        
        Args:
            rows (int): Number of rows to display
        """
        if self.dataframe is None:
            print("No data loaded. Please load an Excel file first.")
            return
        
        print("Data Preview:")
        print(self.dataframe.head(rows))
        print()
    
    def create_nested_structure(self, output_base_path, column_mapping=None):
        """
        Create nested folder/file structure based on DataFrame columns.
        
        Args:
            output_base_path (str): Base path where structure will be created
            column_mapping (dict): Maps column names to folder structure levels
                                  e.g., {'Category': 0, 'Subcategory': 1, 'Item': 'file'}
        """
        if self.dataframe is None:
            print("No data loaded. Please load an Excel file first.")
            return
        
        self.output_base = output_base_path
        
        # If no mapping provided, use default logic
        if column_mapping is None:
            column_mapping = self._auto_detect_mapping()
        
        try:
            os.makedirs(output_base_path, exist_ok=True)
            print(f"Creating structure in: {output_base_path}\n")
            
            created_count = 0
            
            for idx, row in self.dataframe.iterrows():
                current_path = output_base_path
                
                # Iterate through columns (excluding the last one which is typically the file/item)
                for col in self.dataframe.columns[:-1]:
                    value = str(row[col]).strip()
                    
                    if value and value != 'nan':
                        current_path = os.path.join(current_path, value)
                        os.makedirs(current_path, exist_ok=True)
                
                # Create final file if last column is specified as file
                last_col_value = str(row[self.dataframe.columns[-1]]).strip()
                if last_col_value and last_col_value != 'nan':
                    file_path = os.path.join(current_path, f"{last_col_value}.txt")
                    if not os.path.exists(file_path):
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(f"File: {last_col_value}\nCreated from Excel data.\n")
                        created_count += 1
                        print(f"✓ Created: {os.path.relpath(file_path, output_base_path)}")
            
            print(f"\n✓ Structure created successfully!")
            print(f"  Total files/folders created: {created_count}")
            
        except Exception as e:
            print(f"✗ Error creating structure: {e}")
    
    def create_folder_only_structure(self, output_base_path):
        """
        Create only folder structure (no files) based on DataFrame.
        Each row creates a nested folder hierarchy.
        
        Args:
            output_base_path (str): Base path where folders will be created
        """
        if self.dataframe is None:
            print("No data loaded. Please load an Excel file first.")
            return
        
        self.output_base = output_base_path
        
        try:
            os.makedirs(output_base_path, exist_ok=True)
            print(f"Creating folder structure in: {output_base_path}\n")
            
            created_count = 0
            
            for idx, row in self.dataframe.iterrows():
                current_path = output_base_path
                
                # Build nested folder path from all columns
                for col in self.dataframe.columns:
                    value = str(row[col]).strip()
                    
                    if value and value != 'nan':
                        current_path = os.path.join(current_path, value)
                
                # Create the nested structure
                if current_path != output_base_path:
                    os.makedirs(current_path, exist_ok=True)
                    created_count += 1
                    print(f"✓ Created: {os.path.relpath(current_path, output_base_path)}")
            
            print(f"\n✓ Folder structure created successfully!")
            print(f"  Total folders created: {created_count}")
            
        except Exception as e:
            print(f"✗ Error creating folder structure: {e}")
    
    def create_json_structure(self, output_file="structure.json"):
        """
        Export the structure as a JSON file.
        
        Args:
            output_file (str): Path to save the JSON file
        """
        if self.dataframe is None:
            print("No data loaded. Please load an Excel file first.")
            return
        
        try:
            data_dict = self.dataframe.to_dict('records')
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, indent=2, ensure_ascii=False)
            
            print(f"✓ JSON structure saved to: {output_file}")
            
        except Exception as e:
            print(f"✗ Error saving JSON structure: {e}")
    
    def create_csv_mapping(self, output_file="structure_map.csv"):
        """
        Export the structure mapping as CSV.
        
        Args:
            output_file (str): Path to save the CSV file
        """
        if self.dataframe is None:
            print("No data loaded. Please load an Excel file first.")
            return
        
        try:
            self.dataframe.to_csv(output_file, index=False, encoding='utf-8')
            print(f"✓ CSV mapping saved to: {output_file}")
            
        except Exception as e:
            print(f"✗ Error saving CSV mapping: {e}")
    
    def _auto_detect_mapping(self):
        """
        Auto-detect column mapping based on column names.
        
        Returns:
            dict: Mapping of columns to structure levels
        """
        mapping = {}
        for idx, col in enumerate(self.dataframe.columns):
            if idx == len(self.dataframe.columns) - 1:
                mapping[col] = 'file'
            else:
                mapping[col] = idx
        return mapping
    
    def get_structure_tree(self):
        """
        Generate a tree representation of the structure.
        
        Returns:
            str: Tree view of the structure
        """
        if self.output_base is None:
            return "No structure created yet."
        
        tree = []
        for root, dirs, files in os.walk(self.output_base):
            level = root.replace(self.output_base, '').count(os.sep)
            indent = ' ' * 2 * level
            tree.append(f'{indent}{os.path.basename(root)}/')
            
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                tree.append(f'{subindent}{file}')
        
        return '\n'.join(tree)


def main():
    """Main function demonstrating usage."""
    
    print("=" * 60)
    print("Excel to File Structure Generator")
    print("=" * 60)
    print()
    
    # Create an instance
    generator = ExcelToStructure()
    
    # Example usage - modify these paths as needed
    excel_path = input("Enter the path to your Excel file: ").strip()
    
    # Load the Excel file
    if generator.load_excel(excel_path):
        
        # Display preview
        generator.display_preview(rows=5)
        
        # Choose action
        print("\nChoose an option:")
        print("1. Create folder structure only")
        print("2. Create folder + text files structure")
        print("3. Export as JSON")
        print("4. Export as CSV")
        print("5. Display tree structure")
        print()
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            output_path = input("Enter output folder path: ").strip()
            generator.create_folder_only_structure(output_path)
        
        elif choice == '2':
            output_path = input("Enter output folder path: ").strip()
            generator.create_nested_structure(output_path)
        
        elif choice == '3':
            output_file = input("Enter output JSON file path (default: structure.json): ").strip()
            if not output_file:
                output_file = "structure.json"
            generator.create_json_structure(output_file)
        
        elif choice == '4':
            output_file = input("Enter output CSV file path (default: structure_map.csv): ").strip()
            if not output_file:
                output_file = "structure_map.csv"
            generator.create_csv_mapping(output_file)
        
        elif choice == '5':
            if generator.output_base:
                print("\nDirectory Tree:")
                print(generator.get_structure_tree())
            else:
                print("Please create a structure first.")
        
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
