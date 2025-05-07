import re
from smolagents import CodeAgent, InferenceClientModel
from utils.pdf_parser import extract_text_from_pdf 

class AgentCreator:
    def __init__(self):
        self.model = InferenceClientModel() 

    def create_agent_for_section(self, section_name, section_text):
        prompt_templates = {
            "system_prompt": f"You are a resume section extraction agent. Extract structured data from the section: '{section_name}'. Focus on key points and make it concise.",
            "planning": "Plan how you'll parse the section text to extract useful information.",
            "planning.initial_plan": "I will identify the key details under this section and structure them clearly.",
            "managed_agent": "Given the section content, begin your analysis and return a structured output.",
            "final_answer": "Here is the extracted content from the section: {output}"
        }

        agent = CodeAgent(
            tools=[], #can be added later
            model=self.model,
            prompt_templates=prompt_templates,
            grammar=None
        )

        return agent.run(section_text)

    def process_sections(self, text, detected_sections):
        results = {}
        for i, section in enumerate(detected_sections):
            section_text = self.extract_section_text(text, section, detected_sections)
            print(f"\n📌 Processing section: {section}")
            print(f"📄 Section Text Preview: {section_text[:300]}...\n")
            result = self.create_agent_for_section(section, section_text)
            print(f"✅ Extracted Result for '{section}':\n{result}\n")
            results[section] = result
        return results

    def extract_section_text(self, text, section_name, all_sections):
        lines = text.split('\n')
        section_start_index = None
        section_end_index = None

        for i, line in enumerate(lines):
            if line.strip().upper() == section_name.strip().upper():
                section_start_index = i
                break

        if section_start_index is None:
            return ""
            
        for j in range(section_start_index + 1, len(lines)):
            if lines[j].strip().upper() in all_sections:
                section_end_index = j
                break

        section_lines = lines[section_start_index:section_end_index] if section_end_index else lines[section_start_index:]
        return '\n'.join(section_lines)


def extract_section_headers(text):
    lines = text.split("\n")
    pattern = r"^[A-Z][A-Z\s]{2,}$" 
    headers = [line.strip() for line in lines if re.match(pattern, line.strip())]
    return headers


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
