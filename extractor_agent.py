from smolagents import CodeAgent, InferenceClientModel
from utils.pdf_parser import extract_text_from_pdf
import re

class AgentCreator:
    def __init__(self):
        self.model = InferenceClientModel()  # Assuming this model is correctly defined elsewhere

    
    def create_agent_for_section(self, section_name, section_text):
        # Format the agent name and instructions based on the section
        agent_name = f"{section_name.lower().replace(' ', '_')}_extractor"
        instructions = f"Extract details for the section: {section_name}."

        # Define tools (empty list here, adjust if you need specific tools)
        tools = []  # Or provide relevant tools if needed

        # Create agent with the necessary arguments
        agent = CodeAgent(
            tools=tools,        # Provide tools
            model=self.model,   # Provide the model
            prompt_templates=None,  # Optional, you can provide templates if required
            grammar=None,          # Optional, if required
            instructions=instructions  # Pass the instructions as needed
        )
        return agent.run(section_text)
    
    
    def process_sections(self, text, detected_sections):
        # Create a dictionary to store results for each detected section
        results = {}
        for section in detected_sections:
            # Extract the text for each section and pass it to the agent
            section_text = self.extract_section_text(text, section)
            results[section] = self.create_agent_for_section(section, section_text)
        return results
    
    def process_sections(self, text, detected_sections):
      results = {}
      for section in detected_sections:
        # Extract the text for each section and pass it to the agent
        section_text = self.extract_section_text(text, section)
        
        # Debugging print: Check if the section text is extracted correctly
        print(f"Processing section: {section}")
        print(f"Section Text: {section_text[:200]}")  # Print first 200 chars of section text
        
        # Create agent for section and get result
        result = self.create_agent_for_section(section, section_text)
        
        # Debugging print: Check if result from agent is valid
        print(f"Result for section '{section}': {result}")
        
        results[section] = result
      return results


    def extract_section_text(self, text, section_name):
        # Find the start of the section and extract the text until the next newline
        section_start = text.find(section_name)
        section_end = text.find("\n", section_start + len(section_name))
        # Return the text for the section if found, otherwise return an empty string
        return text[section_start:section_end] if section_start != -1 and section_end != -1 else ""

def extract_section_headers(text):
    # Split the text into lines to separate section headers
    lines = text.split("\n")

    # This pattern matches lines that are completely uppercase and may contain spaces between words.
    pattern = r"^[A-Z][A-Z\s]+$"  # Match lines that are all uppercase letters and spaces

    headers = []
    for line in lines:
        if re.match(pattern, line.strip()):  # Match section headers
            headers.append(line.strip())

    # Define possible sections to match against
    possible_sections = [
        "WORK EXPERIENCE", "EXPERIENCE", "EDUCATION", "SKILLS", "CERTIFICATIONS", "PROJECTS",
        "LANGUAGES", "AWARDS", "PUBLICATIONS", "SUMMARY", "EXTRA CURRICULARS"
    ]

    # Filter out headers that are not in the list of possible sections
    return [header for header in headers if header in possible_sections]




class CoordinatorAgent:
    def __init__(self):
        # Initialize the agent creator
        self.agent_creator = AgentCreator()

    def process_cv(self, pdf_path):
    # Extract text from the PDF
       text = extract_text_from_pdf(pdf_path)
       print("\n🔍 Extracted text preview:\n", text[:1000])  # Print the first 1000 characters of the extracted text

    # Detect the sections in the extracted text
       detected_sections = extract_section_headers(text)
       print(f"\n🧩 Detected sections: {detected_sections}")  # Debug print the detected sections

    # Process each section using the agent creator
       section_results = self.agent_creator.process_sections(text, detected_sections)
    
    # Analyze the sentiment of the entire CV (you can replace this with actual sentiment analysis)
       sentiment = self.analyze_sentiment(text)
    
    # Combine the results and return the data
       return {**section_results, "sentiment": sentiment}


    def analyze_sentiment(self, text):
        # Simple placeholder for sentiment analysis; can be replaced with a real sentiment model
        return "neutral"

text = "John Doe\nEXPERIENCE\nWORK EXPERIENCE\nEDUCATION\nSKILLS"
detected_sections = extract_section_headers(text)
print("Detected Sections:", detected_sections)
