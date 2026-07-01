from fastapi import FastAPI
from redis import Redis

app = FastAPI()

# Connect to Redis service in Docker Compose
redis_client = Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

@app.get("/healthz")
def health():
    try:
        redis_client.ping()
        return {
            "status": "ok",
            "redis": "up"
        }
    except:
        return {
            "status": "error",
            "redis": "down"
        }

@app.post("/hit/{key}")
def hit(key: str):
    count = redis_client.incr(key)

    return {
        "key": key,
        "count": count
    }

@app.get("/count/{key}")
def count(key: str):
    value = redis_client.get(key)

    if value is None:
        value = 0

    return {
        "key": key,
        "count": int(value)
    }