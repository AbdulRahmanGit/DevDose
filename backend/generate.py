import google.generativeai as genai
import os
from dotenv import load_dotenv
import typing_extensions
import json
# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Define the schema for the JSON response
class ProgrammingTip(typing_extensions.TypedDict):
    header_title: str
    introduction_greeting: str
    introduction_message: str
    programming_tip_title: str
    programming_tip_description: str
    programming_tip_code: str
    programming_tip_output: str
    dsa_challenge_title: str
    dsa_challenge_problem: str
    dsa_challenge_solution_steps: str
    dsa_challenge_code: str
    footer_message: str

# Initialize the Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": ProgrammingTip,
        "max_output_tokens": 8192,
        "temperature": 0.5
    }, system_instruction="You are a automated Email Generator, you're name is Devdose. you provide Unique info about coding tips and dsa questions and resources"
)

def generate_tips(name, language, difficulty):
    prompt = f'''
    You are an automated email assistant named Devdose, responsible for generating email content. Please generate content for the following placeholders based on the criteria provided:

    1. **Recipient Name**: {name}
    2. **Programming Language**: {language}
    3. **Difficulty Level**: {difficulty}


    Ensure that each piece of content is well-structured, educational, non repititive and engaging. Output the content in JSON format with the following structure:
    {{
        "header_title": f"Devdose Daily Digest - Level Up Your {language} Skills!",
        "introduction_greeting": f"Hello {name},",
        "introduction_message": f"Hope you're having a productive day! Let's dive into some {language} goodness to keep your coding muscles flexing.",
        "programming_tip_title": f"💡 Programming Tip: Practical tip for {language} at the {difficulty} level",
        "programming_tip_description": "Detailed description of a practical tip.",
        "programming_tip_code": "code example",
        "programming_tip_output": "expected output",
        "dsa_challenge_title": f"🔢 DSA Challenge: {language} at the {difficulty} level",
        "dsa_challenge_problem": "Describe the DSA problem.",
        "dsa_challenge_solution_steps": ["Step 1", "Step 2"],  # Ensure this is a list
        "dsa_challenge_code": "solution code",
        "footer_message": f"Keep coding and keep learning, {name}!"
    }}
    '''
    
    try:
        # Generate the content using the model
        response = model.generate_content(prompt)
        
        tips = json.loads(response.text)

        # Print the parsed dictionary for debugging
        #print("Parsed JSON Dictionary:")
        print(tips)
        return tips
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
