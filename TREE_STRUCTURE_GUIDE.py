"""
QUICK START GUIDE - Tree Structure Generator
=============================================

This tool allows you to:
1. Draw/paste a tree structure (even if the folder doesn't exist)
2. Generate actual folders and files based on that structure

THREE WAYS TO USE:
==================

METHOD 1: Using the GUI (Recommended)
--------------------------------------
Run: python tree_structure_generator.py

Steps:
1. Click "Browse Output" to select where to create folders
2. Click "Load Sample 1", "Load Sample 2", or "Load Sample 3" for examples
3. Edit the tree structure if you want
4. Click "Parse Tree" to preview
5. Click "Generate Structure" to create the folders!

METHOD 2: Paste Your Own Tree Structure
---------------------------------------
1. Open tree_structure_generator.py GUI
2. Clear the text area
3. Paste your tree structure (see formats below)
4. Click "Parse Tree" to see preview
5. Click "Generate Structure" to create!

METHOD 3: Load from Text File
-----------------------------
1. Create a .txt file with tree structure
2. Open tree_structure_generator.py GUI
3. Click "Load from File" and select your file
4. Click "Generate Structure"


SUPPORTED TREE FORMATS:
=======================

FORMAT 1: With Tree Characters (Recommended)
---------------------------------------------
MyProject/
├── src/
│   ├── main.py
│   ├── utils.py
│   └── config.py
├── tests/
│   ├── test_main.py
│   └── test_utils.py
├── docs/
│   └── README.md
└── requirements.txt


FORMAT 2: Simple Indentation
-----------------------------
MyProject/
  src/
    main.py
    utils.py
    config.py
  tests/
    test_main.py
    test_utils.py
  docs/
    README.md
  requirements.txt


FORMAT 3: Mixed (Both work together)
------------------------------------
MyProject/
├── src/
│   main.py
│   utils.py
  tests/
    test_main.py
  └── README.md


EXAMPLE USE CASES:
==================

1️⃣ Create a Python Project
---------------------------
python/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py
│       └── decorators.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_utils.py
├── docs/
│   ├── README.md
│   └── API.md
├── venv/
└── requirements.txt


2️⃣ Create a Web Project
------------------------
WebApp/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Button.jsx
│   │   │   ├── Header.jsx
│   │   │   └── Footer.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── About.jsx
│   │   │   └── Contact.jsx
│   │   └── App.jsx
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── routes.py
│   │   ├── models.py
│   │   └── config.py
│   └── requirements.txt
└── README.md


3️⃣ Create Document Organization
---------------------------------
Documents/
├── 2024/
│   ├── January/
│   │   ├── invoices/
│   │   ├── contracts/
│   │   └── reports/
│   ├── February/
│   │   ├── invoices/
│   │   ├── contracts/
│   │   └── reports/
│   └── March/
│       ├── invoices/
│       └── reports/
└── 2025/
    └── January/
        ├── invoices/
        └── reports/


4️⃣ Create Organization Structure
---------------------------------
Company/
├── Engineering/
│   ├── Backend/
│   │   ├── api/
│   │   ├── database/
│   │   └── tests/
│   ├── Frontend/
│   │   ├── components/
│   │   ├── pages/
│   │   └── styles/
│   └── DevOps/
│       ├── docker/
│       ├── kubernetes/
│       └── scripts/
├── Sales/
│   ├── Q1/
│   ├── Q2/
│   ├── Q3/
│   └── Q4/
├── HR/
│   ├── Policies/
│   ├── Training/
│   └── Recruitment/
└── Marketing/
    ├── Campaigns/
    ├── Content/
    └── Analytics/


TIPS & TRICKS:
==============

✅ DO:
- Use trailing "/" for folders (MyFolder/)
- Use simple filenames without slashes (myfile.txt)
- Use indentation to show hierarchy
- Mix tree characters for clarity

❌ DON'T:
- Use special characters in names (use underscore or dash instead)
- Use backslashes in paths
- Create files without extensions (add .txt, .md, etc.)
- Mix different indentation levels inconsistently

KEYBOARD SHORTCUTS:
===================
- Ctrl+A: Select all text in tree area
- Ctrl+C: Copy selected text
- Ctrl+V: Paste tree structure
- Ctrl+Z: Undo (in text editor)


WHAT HAPPENS WHEN YOU GENERATE:
===============================

1. All folders are created
2. All files are created with default placeholder content
3. Nested structures are created automatically
4. No existing files are overwritten
5. Full path is displayed in output log


COMMON QUESTIONS:
=================

Q: Can I edit files after creation?
A: Yes! The created files contain placeholder text. Edit them as needed.

Q: What if I make a mistake in the tree?
A: Use "Parse Tree" to preview. If wrong, edit and parse again before generating.

Q: Can I generate to an existing folder?
A: Yes! It will add new files/folders to existing structure.

Q: What file extensions are supported?
A: Any! .txt, .py, .js, .md, .json, etc. Just type the extension.

Q: Can I use special folders like node_modules?
A: Yes, but they'll be created empty. Usually not recommended.


NEED HELP?
==========

1. Start with a sample (Load Sample 1, 2, or 3)
2. Modify the sample for your needs
3. Click "Parse Tree" to preview
4. Click "Generate Structure" to create


Generated by: Tree Structure Generator
Version: 1.0
"""

if __name__ == "__main__":
    print(__doc__)
