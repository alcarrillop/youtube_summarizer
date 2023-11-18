import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings:
    # Database settings (for future use)
    # DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

    # API settings
    API_V1_STR = "/api/v1"

    # External service configurations
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Add other configurations here

settings = Settings()
