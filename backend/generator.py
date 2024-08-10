from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from formatting import format_code_snippets
from spinner import loading_animation
# Initialize the Codellama model
model = OllamaLLM(model="llama3")

# Define the template for the prompt
template = """
You are an automated email assistant responsible for sending daily reminders to  {{name}}. Please generate content based on the following criteria:

1. **Programming Tips**: Provide {{difficulty}} level tips specifically for {{language}}. Ensure the tips are practical, insightful, and useful for someone at the specified difficulty level.
2. **DSA Questions**: Include {{difficulty}} level DSA questions specifically for {{language}}, along with detailed solutions and explanations.

Format the response clearly and concisely, ensuring it is ready to be included in an email. 

Remember to:
- greet the user by their {{name}} initially and at the end to make it more personalized
- Use appropriate code snippets in {{language}} where necessary.
- make each answer distinct from the previous answer, make it unique. 
- Highlight important points using bold text.
- Ensure the overall content is engaging and educational.

Start generating the content below:
"""
prompt = ChatPromptTemplate.from_template(template)

# Create a chain of the prompt and the model
chain = prompt | model

def generate_tips(name, language, difficulty):
    # Create the context and question for the model
    variables = {"name": name,"language": language, "difficulty": difficulty}
    print("generating content.")
    loading_animation()
    # Invoke the chain with the variables
    result = chain.invoke(variables)
    print("result generated")
    # Format the result to include code snippets properly
    formatted_result = format_code_snippets(result)
    print("Reminder Ready to mail")
    return formatted_result
