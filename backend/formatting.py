import re
from spinner import loading_animation
def format_code_snippets(body):
    """
    Format code snippets enclosed in triple backticks and make text between 
    double asterisks bold with a newline before and after.

    Args:
        body (str): The input text containing code snippets and bold text.

    Returns:
        str: The formatted text with proper code snippet and bold text formatting.
    """
    print("formating is going on...")
    loading_animation(10)
    # Format code snippets
    formatted_body = body.replace('```', '<pre class="code-snippet"><code>').replace('```', '</code></pre>')
    
    # Format bold  (text between **)
    formatted_body = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_body)
    
    # Add new lines before and after bold text
    formatted_body = re.sub(r'(<strong>.*?</strong>)', r'\n\1\n', formatted_body)
    print("formating Done")
    return formatted_body
