# CV_Parsing_Agentic_AI

This project uses **Agentic AI** to extract data from resumes that are in PDF format by identifying sections such as **Experience**, **Education**, **Skills**, etc.

As I was given a chance to think out box, instead of going in a tradition way and using a single agent architecture I want ahead with a mutli agent architecture.

My first idea of single agent architecture was to give PDFs as input to the PDF text extractor,then give it to the field extractor agent (using smolagent) and later give output in JSON format.

Taking a multi agent architecture would help me concentrate more on extracting sections more feasibly and work on giving the output according to specific sections, hence by creating agents to each section would make it easy to extract.
but there were few crucial points that I thoguht of when this is used as a real world example,

PDF extracts text that can be different sections other than the basic section names. (Like Internships, Participations etc)
So I wanted to create an automated agent that creates agents for the extracted sections keeping basic agents like cordination agent (Extracting agent can also be created)

Problem to be exlpored(which I did not include in the scope of this problem) : If there are words similar to the section names, then need to be carefull with the extraction of sections (while using regex)

main.py - this is the main file that runs the command line arguments and runs the coordination agent (which runs all the agents)
extractor_agent.py - this contaisn all the agent definations and logic
pdf_parser.py - this extracts the text from pdfs (I did not add any agent here keeping it simple)

