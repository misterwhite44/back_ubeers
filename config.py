import os
from dotenv import load_dotenv

load_dotenv()

front_url = os.getenv("FRONT_URL")

class Config:
    REDIS_HOST = os.getenv("REDIS_HOST", front_url)
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))

    DB_CONFIG = {
        'host': os.getenv("DB_HOST"),
        'port': int(os.getenv("DB_PORT", 3306)),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'database': os.getenv("DB_NAME"),
        'charset': os.getenv("DB_CHARSET", 'utf8mb4')

    
}
SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset={DB_CONFIG['charset']}"
)