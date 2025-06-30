import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_db = os.getenv("REDIS_DB")

if not redis_host or not redis_port or not redis_db:
    raise RuntimeError("Les variables REDIS_HOST, REDIS_PORT et REDIS_DB doivent être définies")

redis_client = redis.Redis(
    host=redis_host,
    port=int(redis_port),
    db=int(redis_db),
    decode_responses=True
)
