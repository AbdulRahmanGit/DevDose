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
    dsa_problem_links:str
    footer_message: str

# Initialize the Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config={
        "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
    }, system_instruction="You are a automated Email Generator, you're name is Devdose. you provide info for each user  about coding tips and dsa questions and resources"
)

def generate_tips(name, language, difficulty):
    prompt = f'''
You are an automated email assistant named Devdose, responsible for generating unique and engaging email content for users based on their programming language and skill level. Please generate content using the following placeholders:

1. **Recipient Name**: {name}
2. **Programming Language**: {language}
3. **Difficulty Level**: {difficulty}

The content should be well-structured, educational, non-repetitive, and tailored to the specified language and difficulty level. Output the content in JSON format with the following structure:

{{
    "header_title": f"Devdose Daily Digest - Level Up Your {language} Skills!",
    "introduction_greeting": f"Hello {name},",
    "introduction_message": f"Hope you're having a productive day! Let's dive into some {language} goodness to keep your coding muscles flexing",
    "programming_tip_title": f"Programming Tip: Practical tip for {language} at the {difficulty} level",
    "programming_tip_description": f"Provide a unique,  and detailed programming tip tailored to {language} and the {difficulty} level, Ensure this tip is non-repetitive and insightful",
    "programming_tip_code": "Include a concise code example that demonstrates the tip in action",
    "programming_tip_output": "Show the expected output of the code example",
    "dsa_challenge_title": f" DSA Challenge: {language} at the {difficulty} level",
    "dsa_challenge_problem": f"Describe a unique Data Structures and Algorithms (DSA) problem relevant to {language} at the {difficulty} level",
    "dsa_challenge_solution_steps": [
        "Step 1: Describe the first step to solve the problem",
        "Step 2: Describe the second step to solve the problem",
        "Step 3: Describe the third step to solve the problem"
    ],
    "dsa_challenge_code": "Provide the full solution code for the problem",
    "dsa_problem_links": "Provide a unique link to a relevant LeetCode problem matching the {difficulty} level, Ensure the problem is different each time",
    "footer_message": f"Keep coding and keep learning, {name}!"
}}

Please ensure that each field is filled with thoughtful and non-repetitive content, focusing on practical application and real-world relevance
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
