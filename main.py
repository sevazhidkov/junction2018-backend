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
    return jsonify({x: y() for x, y in measurements.items()})


@app.route('/last_message')
def last_message_handler():
    return {'message': messages.last_message(redis, 0)}


if int(os.environ.get('DEBUG', 1)) == 1:
    app.run(debug=True)
