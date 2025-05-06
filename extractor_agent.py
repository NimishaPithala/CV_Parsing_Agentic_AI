from smolagents import CodeAgent, InferenceClientModel
from utils.pdf_parser import extract_text_from_pdf
import re

class AgentCreator:
    def __init__(self):
        self.model = InferenceClientModel()  

    
    def create_agent_for_section(self, section_name, section_text):
        agent_name = f"{section_name.lower().replace(' ', '_')}_extractor"
        instructions = f"Extract details for the section: {section_name}."
        tools = []  

        agent = CodeAgent(
            tools=tools,       
            model=self.model,  
            prompt_templates=None,  
            grammar=None,          
            instructions=instructions 
        )
        return agent.run(section_text)
    
    
    def process_sections(self, text, detected_sections):
        results = {}
        for section in detected_sections:
            section_text = self.extract_section_text(text, section)
            results[section] = self.create_agent_for_section(section, section_text)
        return results
    
    def process_sections(self, text, detected_sections):
      results = {}
      for section in detected_sections:
        section_text = self.extract_section_text(text, section)
    
        print(f"Processing section: {section}")
        print(f"Section Text: {section_text[:200]}") 
        
        result = self.create_agent_for_section(section, section_text)
        
    
        print(f"Result for section '{section}': {result}")
        
        results[section] = result
      return results


    def extract_section_text(self, text, section_name):
        section_start = text.find(section_name)
        section_end = text.find("\n", section_start + len(section_name))
        return text[section_start:section_end] if section_start != -1 and section_end != -1 else ""

def extract_section_headers(text):
    lines = text.split("\n")
    pattern = r"^[A-Z][A-Z\s]+$"  

    headers = []
    for line in lines:
        if re.match(pattern, line.strip()):  
            headers.append(line.strip())

"""
def extract_section_headers(text):
    lines = text.split("\n")
    pattern = r"^[A-Z][A-Z\s]+$"
    headers = [line.strip() for line in lines if re.match(pattern, line.strip())]
    return headers 
"""
    
    possible_sections = [
        "WORK EXPERIENCE", "EXPERIENCE", "EDUCATION", "SKILLS", "CERTIFICATIONS", "PROJECTS",
        "LANGUAGES", "AWARDS", "PUBLICATIONS", "SUMMARY", "EXTRA CURRICULARS"
    ]
    return [header for header in headers if header in possible_sections]


class CoordinatorAgent:
    def __init__(self):
        
        self.agent_creator = AgentCreator()

    def process_cv(self, pdf_path):
       text = extract_text_from_pdf(pdf_path)
       print("\n🔍 Extracted text preview:\n", text[:1000])  

       detected_sections = extract_section_headers(text)
       print(f"\n🧩 Detected sections: {detected_sections}")  
       section_results = self.agent_creator.process_sections(text, detected_sections)
    
       sentiment = self.analyze_sentiment(text)

       return {**section_results, "sentiment": sentiment}


    def analyze_sentiment(self, text):
        return "neutral"

text = "John Doe\nEXPERIENCE\nWORK EXPERIENCE\nEDUCATION\nSKILLS"
detected_sections = extract_section_headers(text)
print("Detected Sections:", detected_sections)
