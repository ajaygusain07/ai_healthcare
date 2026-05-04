from pydantic_settings import BaseSettings

class Settings(BaseSettings):#this function is used to create the settings schema for the application and it will be used in the database.py file to connect to the database and it will be used in the api files to perform database operations and it will be used in the auth.py file to perform authentication operations and it will be used in the main.py file to run the application
    APP_NAME: str = "Health Chatbot API"
    DEBUG: bool = False
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "healthchatbot"
    JWT_EXPIRE_MINUTES: int = 1440 
    JWT_SECRET_KEY: str = "change_this_in_production"
    JWT_ALGORITHM: str = "HS256"
    GEMINI_API_KEY: str = ""
    CHROMA_DB_PATH: str = "./chroma_db"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    TOP_K_RESULTS: int = 5
    GROQ_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()