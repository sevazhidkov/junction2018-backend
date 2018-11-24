import random
import sys
import time

from sender import answer_message

type = sys.argv[1]

if type == 'message':
    answer_message(message_type=sys.argv[2])
elif type == 'random':
    while True:
        answer_message(message_type=random.choice(['door_open', 'temperature_change', 'too_many_person', 'new_person']))
        time.sleep(random.randint(1, 20) / 10)
