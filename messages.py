from redis import Redis
import time

messages_dict = {
    'close_door': 'Someone has forgotten to close the door please fix it boy'
}


def last_message(redis: Redis, user_id):
    while redis.llen(user_id) == 0:
        time.sleep(0.01)
        continue
    return redis.lpop(user_id)


def save_message(redis: Redis, user_id, message_id, to_format=None):
    if to_format is None:
        to_format = []
    redis.lpush(user_id, messages_dict[message_id].format(*to_format))
