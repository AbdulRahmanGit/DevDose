demo https://github.com/AbdulRahmanGit/DevDose/blob/main/demo.gif

---

# DevDoses

DevDoses is an automated email tool designed to provide personalized programming tips and Data Structures and Algorithms (DSA) questions. The system leverages language models to generate tailored content based on user preferences, enhancing learning and engagement.

## Features

- **Automated Email Generation**: Send daily emails with programming tips and DSA questions.
- **Personalized Content**: Content is customized based on user preferences such as programming language and difficulty level.
- **Integration with PostgreSQL**: Stores user data and preferences in a PostgreSQL database.
- **Use of Language Models**: Generates insightful and practical programming tips and DSA questions.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL
- Git

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/AbdulRahmanGit/LLM-Email-Automation.git
   cd LLM-Email-Automation
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory of the project. Add your API keys and database credentials to this file:

   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/yourdatabase
   API_KEY=your_api_key
   ```

   Replace `username`, `password`, `localhost`, `5432`, `yourdatabase`, and `your_api_key` with your actual PostgreSQL credentials and API key.

5. **Configure the Application**

   Ensure the `.env` file is correctly loaded. The application uses `python-dotenv` to read environment variables from the `.env` file.

6. **Run the Application**

   Start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

   The application will be accessible at `http://127.0.0.1:8000`.

### Usage

1. **Register Users**

   Access the user registration page at `/register` to add new users.

2. **Send Emails**

   Set up scheduled tasks to run the email sender script. The emails will include programming tips and DSA questions based on user preferences.

### Project Structure

- `main.py`: Entry point for the FastAPI application.
- `db.py`: Database models and queries.
- `email_sender.py`: Script for sending automated emails.
- `config.py`: Configuration file for application settings.
- `.env`: Environment variables for API keys and database credentials.
- `requirements.txt`: List of Python dependencies.

### Contributing

If you'd like to contribute to DevDoses, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contact

For any inquiries or feedback, please reach out to [Abdul Rahman](mailto:abdulrahman@example.com).

---

Feel free to adjust the file paths or additional details according to your project’s specifics!
