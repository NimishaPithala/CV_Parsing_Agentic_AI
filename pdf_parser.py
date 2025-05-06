import fitz  

def extract_text_from_pdf(pdf_path):
    print("inside the loop")
    doc = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(doc.page_count):
        print(f"Reading page {page_num + 1}")
        page = doc.load_page(page_num)
        page_text = page.get_text("text")
        print(f"Page {page_num + 1} length: {len(page_text)} characters")
        text += page_text

    print("Extraction complete.")
    return text

pdf_path = "C:/Users/Administrator/Desktop/CV_Parsing_AgenticAI/sample_data/Deedy_Resume_Reversed__1_.pdf"
text = extract_text_from_pdf(pdf_path)

