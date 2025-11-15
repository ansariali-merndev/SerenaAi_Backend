from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_URI = getenv("DATABASEURI")
SECRET_KEY = getenv("SECRET_KEY")
FRONTEND_URI = getenv("FRONTEND_URI")
GEMINI_API_KEY = getenv("GEMINI_API_KEY")
GROQ_API_KEY = getenv("GROQ_API_KEY")