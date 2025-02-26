from dotenv import load_dotenv
import os

load_dotenv(override=True)

WEB_URL = os.getenv("WEB_URL") 
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET") 
DB_HOST = os.getenv("DB_HOST") 
DB_USERNAME = os.getenv("DB_USERNAME") 
DB_NAME = os.getenv("DB_NAME") 
DB_PASSWORD = os.getenv("DB_PASSWORD") 
PANEL_URL = os.getenv("PANEL_URL")
PANEL_API = os.getenv("PANEL_API")