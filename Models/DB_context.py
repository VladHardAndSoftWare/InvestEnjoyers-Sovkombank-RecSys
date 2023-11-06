import os

from dotenv import load_dotenv
# from sqlalchemy import create_engine

load_dotenv()
DB_CONN = os.environ['DB_CONN']