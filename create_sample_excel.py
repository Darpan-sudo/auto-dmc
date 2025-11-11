"""
Create sample Excel files for testing the GUI
"""

import pandas as pd
import os


def create_sample_excel_1():
    """Create a simple project structure example."""
    data = {
        'Project': ['Website', 'Website', 'Website', 'Mobile App', 'Mobile App', 'Mobile App'],
        'Category': ['Frontend', 'Backend', 'Database', 'iOS', 'Android', 'Backend'],
        'Task': ['HTML Templates', 'API Server', 'Schema Design', 'UI Components', 'Activities', 'API Integration']
    }
    
    df = pd.DataFrame(data)
    df.to_excel('example_project_structure.xlsx', index=False)
    print("✓ Created: example_project_structure.xlsx")
    return df


def create_sample_excel_2():
    """Create a document classification example."""
    data = {
        'Department': ['HR', 'HR', 'Finance', 'Finance', 'IT', 'IT', 'Marketing', 'Marketing'],
        'Year': ['2024', '2025', '2024', '2025', '2024', '2025', '2024', '2025'],
        'Document Type': ['Policies', 'Training', 'Budget', 'Reports', 'Maintenance', 'Projects', 'Campaigns', 'Analytics']
    }
    
    df = pd.DataFrame(data)
    df.to_excel('example_document_structure.xlsx', index=False)
    print("✓ Created: example_document_structure.xlsx")
    return df


def create_sample_excel_3():
    """Create a product catalog example."""
    data = {
        'Category': ['Electronics', 'Electronics', 'Electronics', 'Furniture', 'Furniture', 'Clothing', 'Clothing'],
        'Subcategory': ['Phones', 'Laptops', 'Accessories', 'Chairs', 'Tables', 'Shirts', 'Pants'],
        'Brand': ['Samsung', 'Dell', 'Apple', 'IKEA', 'Herman Miller', 'Nike', 'Adidas'],
        'Item': ['S24', 'XPS', 'AirPods', 'Markus', 'Eames', 'DriFit', 'Ultraboost']
    }
    
    df = pd.DataFrame(data)
    df.to_excel('example_product_catalog.xlsx', index=False)
    print("✓ Created: example_product_catalog.xlsx")
    return df


def create_sample_excel_4():
    """Create a company structure example."""
    data = {
        'Company': ['TechCorp', 'TechCorp', 'TechCorp', 'TechCorp', 'TechCorp', 'TechCorp'],
        'Division': ['Engineering', 'Engineering', 'Sales', 'Sales', 'Operations', 'Operations'],
        'Department': ['Backend', 'Frontend', 'Enterprise', 'SMB', 'Finance', 'HR'],
        'Team': ['Core', 'Web', 'B2B', 'Retail', 'Accounting', 'Recruitment']
    }
    
    df = pd.DataFrame(data)
    df.to_excel('example_org_structure.xlsx', index=False)
    print("✓ Created: example_org_structure.xlsx")
    return df


def create_sample_excel_5():
    """Create a course curriculum example."""
    data = {
        'University': ['State University'] * 6,
        'Faculty': ['Engineering', 'Engineering', 'Science', 'Science', 'Arts', 'Arts'],
        'Program': ['CS', 'Civil', 'Physics', 'Chemistry', 'English', 'History'],
        'Course': ['Data Structures', 'Mechanics', 'Quantum', 'Organic', 'Literature', 'Medieval']
    }
    
    df = pd.DataFrame(data)
    df.to_excel('example_course_structure.xlsx', index=False)
    print("✓ Created: example_course_structure.xlsx")
    return df


def display_examples():
    """Display all examples."""
    print("\n" + "="*70)
    print("SAMPLE EXCEL FILES FOR EXCEL TO STRUCTURE GENERATOR")
    print("="*70 + "\n")
    
    # Example 1
    print("📁 EXAMPLE 1: Project Structure")
    print("-" * 70)
    df1 = create_sample_excel_1()
    print("\nData Preview:")
    print(df1.to_string(index=False))
    print("\n\nOutput Structure:")
    print("""
    output_folder/
    ├── Website/
    │   ├── Frontend/
    │   │   └── HTML Templates.txt
    │   ├── Backend/
    │   │   └── API Server.txt
    │   └── Database/
    │       └── Schema Design.txt
    └── Mobile App/
        ├── iOS/
        │   └── UI Components.txt
        ├── Android/
        │   └── Activities.txt
        └── Backend/
            └── API Integration.txt
    """)
    
    # Example 2
    print("\n" + "="*70)
    print("📁 EXAMPLE 2: Document Classification")
    print("-" * 70)
    df2 = create_sample_excel_2()
    print("\nData Preview:")
    print(df2.to_string(index=False))
    print("\n\nOutput Structure:")
    print("""
    output_folder/
    ├── HR/
    │   ├── 2024/
    │   │   └── Policies.txt
    │   └── 2025/
    │       └── Training.txt
    ├── Finance/
    │   ├── 2024/
    │   │   └── Budget.txt
    │   └── 2025/
    │       └── Reports.txt
    ├── IT/
    │   ├── 2024/
    │   │   └── Maintenance.txt
    │   └── 2025/
    │       └── Projects.txt
    └── Marketing/
        ├── 2024/
        │   └── Campaigns.txt
        └── 2025/
            └── Analytics.txt
    """)
    
    # Example 3
    print("\n" + "="*70)
    print("📁 EXAMPLE 3: Product Catalog")
    print("-" * 70)
    df3 = create_sample_excel_3()
    print("\nData Preview:")
    print(df3.to_string(index=False))
    print("\n\nOutput Structure (Folders Only):")
    print("""
    output_folder/
    ├── Electronics/Phones/Samsung/Samsung.txt
    ├── Electronics/Laptops/Dell/Dell.txt
    ├── Electronics/Accessories/Apple/Apple.txt
    ├── Furniture/Chairs/IKEA/IKEA.txt
    ├── Furniture/Tables/Herman Miller/Herman Miller.txt
    ├── Clothing/Shirts/Nike/Nike.txt
    └── Clothing/Pants/Adidas/Adidas.txt
    """)
    
    # Example 4
    print("\n" + "="*70)
    print("📁 EXAMPLE 4: Organization Structure")
    print("-" * 70)
    df4 = create_sample_excel_4()
    print("\nData Preview:")
    print(df4.to_string(index=False))
    
    # Example 5
    print("\n" + "="*70)
    print("📁 EXAMPLE 5: Course Curriculum")
    print("-" * 70)
    df5 = create_sample_excel_5()
    print("\nData Preview:")
    print(df5.to_string(index=False))
    
    print("\n" + "="*70)
    print("✓ All sample Excel files have been created!")
    print("="*70)
    print("\n📝 Usage Instructions:")
    print("1. Run this script: python create_sample_excel.py")
    print("2. Open the GUI: python excel_to_structure_gui.py")
    print("3. Click 'Browse Input' and select any example_*.xlsx file")
    print("4. Click 'Load Excel' to see the data")
    print("5. Customize options and click 'Generate Structure'")
    print("\n")


if __name__ == "__main__":
    display_examples()
