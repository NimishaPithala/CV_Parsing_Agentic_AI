import sys
print(sys.executable)

import sys
import json
from pdf_parser import extract_text_from_pdf
from extractor_agent import CoordinatorAgent

def main(pdf_path: str, output_path: str):
    print("[INFO] Starting CV processing")
    coordinator = CoordinatorAgent()
    result_json = coordinator.process_cv(pdf_path)  # Process the CV and get the extracted data

    # Debugging print: Check if result_json contains valid data
    print(f"Final result to be saved: {result_json}")
    
    # Save the results to a JSON file
    with open(output_path, 'w') as f:
        json.dump(result_json, f, indent=2)
    
    print(f"[SUCCESS] Output saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_pdf_path> <output_json_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    #pdf_path = "C:/Users/Administrator/Desktop/CV_Parsing_AgenticAI/sample_data/Deedy_Resume_Reversed__1_.pdf"
    #output_path = "C:/Users/Administrator/Desktop/CV_Parsing_AgenticAI/output_data/output.json"
    main(pdf_path, output_path)
