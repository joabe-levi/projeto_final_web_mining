import os
from dotenv import load_dotenv

load_dotenv() 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.getenv("db_path", os.path.join(BASE_DIR, "data", "dck.db"))
