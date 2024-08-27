from database import SessionLocal, get_db, fetch_users, User, fetch_user
from email_utils import send_email
from generate import generate_tips
from jinja2 import Template
import os
def test():
    db = SessionLocal()
    try:
        user = fetch_user(db, "rahmanweb4@gmail.com")
        if not user:
            print("No users found.")
            return

        if user:
            try:
                name, email, language, difficulty = user.name, user.email, user.language, user.difficulty
                tips = generate_tips(name, language, difficulty)
                # Ensure the template file exists
                template_path = os.path.join(os.path.dirname(__file__), 'template.html')

                if os.path.isfile(template_path):
                    print(f"Template file found at: {template_path}")
                    
                    with open(template_path) as file:
                        template = Template(file.read())

                    # Define subject separately and render with the template
                    subject = f"Devdose Daily Digest - Level Up Your {difficulty} {language} Skills!"
                    unsubscribe_link = f"https://devdose.vercel.app/templates/delete.html"
                    update_link = f"https://devdose.vercel.app/templates/update.html"
                     
                    context = {
                        "header_title": tips.get("header_title", ""),
                        "introduction_greeting": tips.get("introduction_greeting", ""),
                        "introduction_message": tips.get("introduction_message", ""),
                        "programming_tip_title": tips.get("programming_tip_title", ""),
                        "programming_tip_description": tips.get("programming_tip_description", ""),
                        "programming_tip_code": tips.get("programming_tip_code", ""),
                        "programming_tip_output": tips.get("programming_tip_output", ""),
                        "dsa_challenge_title": tips.get("dsa_challenge_title", ""),
                        "dsa_problem_links":tips.get("dsa_problem_links", ""),
                        "dsa_challenge_problem": tips.get("dsa_challenge_problem", ""),
                        "dsa_challenge_solution_steps": tips.get("dsa_challenge_solution_steps", []),  # Ensure this is a list
                        "dsa_challenge_code": tips.get("dsa_challenge_code", ""),
                        "footer_message": tips.get("footer_message", ""),
                    }
    

                    try:
                        html_content = template.render(context, unsubscribe_link= unsubscribe_link, update_link=update_link)
                        send_email(subject, html_content, email)
                    except Exception as e:
                        print(f"Error rendering template: {e}")
                else:
                    print(f"Template file not found at: {template_path}")


            except Exception as e:
                print(f"Error processing user {user.name}: {e}")
                # Optionally, log the error or notify someone

    except Exception as e:
        print(f"Error in job execution: {e}")
        # Optionally, log the error or notify someone

    finally:
        db.close()
test()