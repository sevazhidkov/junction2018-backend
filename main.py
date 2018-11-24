import json
import os

from flask import Flask, jsonify, redirect, url_for
from redis import Redis
from measures import measurements, get_measurement, get_sensor_data, reset
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
    redis.expire('m_cache', 60 * 30)

    reset()

    return jsonify(response)


@app.route('/m_cache')
def m_cache_handler():
    r_resp = redis.get('m_cache')
    if r_resp:
        return jsonify(json.loads(redis.get('m_cache').decode('utf-8')))
    else:
        return redirect(url_for('measure_handler'), code=302)


@app.route('/last_message')
def last_message_handler():
    return jsonify({'message': messages.last_message(redis, 0).decode('utf-8')})


@app.route('/last_measurements')
def last_measurements_handler():
    return jsonify({'measurements': list(map(get_measurement, get_sensor_data('Bench2', 100)))})


if int(os.environ.get('DEBUG', 1)) == 1:
    app.run(debug=True)
