import os
import json
import ollama
import pandas as pd
from docx import Document 

# --- 1. CONFIGURATION ---

# !!! CHANGE THIS TO THE FOLDER CONTAINING YOUR .adoc AND .docx FILES !!!
INPUT_FOLDER = "D:\\Projects\\auto-dmc\\documents" 

INFO_CODES_FILE = r'data\info_codes.json'
LLM_MODEL = "llama3.1:8b" # Change this to the model you have pulled in Ollama (e.g., 'mistral', 'phi3')
OUTPUT_CSV_FILE = 'document_info_codes.csv'

# --- END CONFIGURATION ---


# --- 2. LOAD THE INFO CODE STANDARD ---

try:
    # Look for info_codes.json in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    info_codes_path = os.path.join(script_dir, INFO_CODES_FILE)
    
    with open(info_codes_path, 'r', encoding='utf-8') as f:
        info_data = json.load(f)
except Exception as e:
    print(f"Error loading info codes: {e}")
    exit()

# Format the entire list into a string for the LLM prompt
CLASSIFICATION_LIST = ""
for item in info_data:
    CLASSIFICATION_LIST += f"{item['code']}: {item['title']}\n"


# --- 3. DOCUMENT TEXT EXTRACTION FUNCTION ---

def extract_text(filepath):
    """Extracts text content from .adoc or .docx files."""
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if ext == '.adoc':
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Read max 16KB of text for better context
                return f.read(16384)
        except Exception:
            return "Error reading .adoc file"

    elif ext == '.docx':
        try:
            doc = Document(filepath)
            content = '\n'.join([p.text for p in doc.paragraphs])
            # Read max 16KB of text for better context
            return content[:16384]
        except Exception:
            return "Error reading .docx file"
    
    return "Unsupported file type"


# --- 4. OLLAMA GENERATION FUNCTION (Improved) ---

def generate_info_code_with_ollama(document_text, model=LLM_MODEL):
    """
    Calls Ollama to classify the document text against the provided standard.
    Returns the 3-digit code string with improved accuracy.
    """
    if document_text.startswith("Error") or document_text == "Unsupported file type":
        return "ERROR"

    system_prompt = (
        "You are a highly specialized technical document classifier with expertise in maintenance documentation standards. "
        "Your sole task is to analyze the DOCUMENT CONTENT and match its primary purpose to the SINGLE MOST RELEVANT "
        "3-digit code from the INFO CODE LIST provided below. "
        "\n\nClassification Rules:"
        "\n- Focus on the document's PRIMARY PURPOSE, not secondary content"
        "\n- Match FUNCTIONAL INTENT (what the document does/describes)"
        "\n- If describing a component or system design/function: use 030-090 range (descript types)"
        "\n- If describing operational procedures: use 100-180 range (proced types)"
        "\n- If describing maintenance/servicing: use 200-299 range (proced types)"
        "\n- If describing testing/inspection: use 300-399 range (proced types)"
        "\n- If describing troubleshooting/fault isolation: use 400-449 range (fault types)"
        "\n- If describing removal/disassembly: use 500-563 range (proced types)"
        "\n- If describing repairs: use 600-687 range (mixed types)"
        "\n\nOutput Requirements:"
        "\n- MUST output ONLY a 3-digit code (e.g., '042', '210', '280')"
        "\n- Do not include any other text, punctuation, or explanation"
        "\n- If no clear match exists, output '910'"
    )
    
    prompt = f"{system_prompt}\n\n"
    prompt += "--- INFO CODE LIST ---\n"
    prompt += CLASSIFICATION_LIST
    prompt += "\n--- END LIST ---\n\n"
    prompt += f"DOCUMENT CONTENT TO CLASSIFY:\n---\n{document_text}\n---\n\n"
    prompt += "OUTPUT THE 3-DIGIT CODE ONLY:"
    
    try:
        # Use low temperature for deterministic classification
        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={"temperature": 0.1, "seed": 42, "top_k": 10, "top_p": 0.3}
        )
        
        # Clean up the output to get just the code
        info_code = response['response'].strip().upper()
        
        # Extract only digits if there's extra text
        digits = ''.join(c for c in info_code if c.isdigit())
        
        if len(digits) >= 3:
            # Take the first 3 digits
            info_code = digits[:3]
        
        # Validate the code exists in our list
        if len(info_code) == 3 and info_code.isdigit():
            # Check if code exists in our data
            if any(item['code'] == info_code for item in info_data):
                return info_code
            else:
                # Code doesn't exist, return 910
                return "910"
        else:
            return "910"

    except Exception as e:
        print(f"  Warning: LLM error - {e}")
        return "OLLAMA_ERR"

# --- 5. MAIN EXECUTION (Updated to traverse folder) ---

if __name__ == "__main__":
    
    results = []
    files_to_process = []
    
    print(f"Searching for .adoc and .docx files in: {INPUT_FOLDER}")
    
    # Traverse the input folder and find all supported files
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(('.adoc', '.docx')):
            files_to_process.append(os.path.join(INPUT_FOLDER, filename))

    if not files_to_process:
        print("No .adoc or .docx files found in the specified folder.")
        exit()

    for filepath in files_to_process:
        filename = os.path.basename(filepath)
        print(f"\nProcessing: {filename}...")
        
        # Step A: Extract Text
        doc_content = extract_text(filepath)
        
        if doc_content.startswith("Error"):
            print(f" -> ERROR: Could not read file")
            results.append({
                'File_Name': filename,
                'Info_Code': 'ERROR',
                'Code_Title': 'N/A',
                'Code_Type': 'N/A'
            })
            continue
        
        # Step B: Generate Code
        info_code = generate_info_code_with_ollama(doc_content)
        
        if info_code == "OLLAMA_ERR":
            print(f" -> ERROR: LLM service unavailable")
            results.append({
                'File_Name': filename,
                'Info_Code': 'OLLAMA_ERR',
                'Code_Title': 'N/A',
                'Code_Type': 'N/A'
            })
            continue
        
        # Step C: Look up details from the JSON list
        match = next((item for item in info_data if item['code'] == info_code), 
                     {'code': info_code, 'title': 'N/A', 'type': 'N/A'})
        
        # Step D: Store Result
        results.append({
            'File_Name': filename,
            'Info_Code': match['code'],
            'Code_Title': match['title'],
            'Code_Type': match['type']
        })
        
        print(f" -> Result: {match['code']} ({match['title']})")

    # Step E: Create DataFrame and save to CSV
    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT_CSV_FILE), index=False)
        
        print("\n--- RESULTS ---")
        print(f"Successfully generated and saved results to: {OUTPUT_CSV_FILE}")
        
    else:
        # This should only happen if files_to_process was empty, which is checked earlier
        print("No files were processed.")