from redis import Redis
import time


def last_message(redis: Redis, user_id):
    while redis.llen(user_id) == 0:
        time.sleep(0.1)
        continue
    return redis.lpop(user_id)


def save_message(redis: Redis, user_id, message):
    redis.lpush(user_id, message)
