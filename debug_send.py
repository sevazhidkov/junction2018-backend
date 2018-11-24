import random
import sys
import time

from anomaly_detect import sensors
from sender import answer_message

type = sys.argv[1]

if type == 'message':
    answer_message(message_type=sys.argv[2])
elif type == 'random':
    while True:
        answer_message(message_type=random.choice([x['message_type'] for x in sensors]))
        time.sleep(random.randint(5, 20))
