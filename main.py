import json
import os

from flask import Flask, jsonify
from redis import Redis
from measures import measurements
import messages

app = Flask(__name__)
redis = Redis(db=1)


@app.route('/')
def main_handler():
    return jsonify({'success': True})


@app.route('/reset')
def reset_handler():
    redis.delete(0)
    return jsonify({'success': True})


@app.route('/measurements')
def measure_handler():
    response = {x: '%.1f' % round(y(), 1) for x, y in measurements.items()}
    redis.set('m_cache', json.dumps(response))
    redis.expire('m_cache', 60*30)

    return jsonify(response)


@app.route('/m_cache')
def m_cache_handler():
    return jsonify(json.loads(redis.get('m_cache').decode('utf-8')))  # Add saving to cache in measurements handler


@app.route('/last_message')
def last_message_handler():
    return jsonify({'message': messages.last_message(redis, 0).decode('utf-8')})


if int(os.environ.get('DEBUG', 1)) == 1:
    app.run(debug=True)
