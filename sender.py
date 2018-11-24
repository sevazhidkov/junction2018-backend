from messages import save_message
from redis import Redis

redis = Redis(db=1)


def answer_message(message_type):
    if message_type == 'door_open':
        save_message(redis, 0, 'Door is open! Close it right now.')
        return

    if message_type == 'temperature_change':
        save_message(redis, 0, 'Oh it seems like the Temperature is changing')
        return

    if message_type == 'too_many_person':
        save_message(redis, 0, 'Too many person in the room')
        return

    if message_type == 'new_person':
        save_message(redis, 0, "Hi! Nice to meet you! I'm talking sauna.")
        return
