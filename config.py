import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
