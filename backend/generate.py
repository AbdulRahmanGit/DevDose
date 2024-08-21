import google.generativeai as genai
import os
from spinner import loading_animation
from dotenv import load_dotenv
from formatting import format_code_snippets
import time
# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_tips(name, language, difficulty):
    # Create the context and question for the model
    prompt = f'''
    You are an automated email assistant by the name DevDoses responsible for sending daily reminders to {name}. Please generate content based on the following criteria:

    1. **Programming Tips**: Provide tips specifically for {language} at the {difficulty} level. Ensure the tips are practical, insightful, and useful for someone at the specified difficulty level. Use appropriate code snippets in {language} where necessary.
    
    2. **DSA Questions**: Include DSA questions relevant to {language} at the {difficulty} level. Provide detailed solutions and explanations for each question. The questions should be suited to the {difficulty} level specified.
    - Greet {name} initially and at the end to make it more personalized.
    - Highlight important points using bold text.
    - Add Leetcode Problems that match the difficulty level.
    - Ensure the overall content is engaging, educational, and formatted clearly for inclusion in an email.
    
    '''

    print("Generating email content for all registered users.")
    loading_animation(1)  # Assuming this is a custom function you have
    time.sleep(1)
    # Invoke the Gemini model to generate content
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            max_output_tokens=1000,
            temperature=0.1,
        )
    )
    print("Result generated")
    # Format the result to include code snippets properly
    formatted_result = format_code_snippets(response.text)  # Assuming this is a custom function you have

    print("Reminder ready to mail")
    return formatted_result
#generate_tips("anas", "java", "mid senior level")






