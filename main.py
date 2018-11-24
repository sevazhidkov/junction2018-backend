import json
import os

from flask import Flask, jsonify, redirect, url_for, request
from redis import Redis
from measures import measurements, get_measurement, get_sensor_data, reset
import messages
from talk import analyze_message

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
    message = messages.last_message(redis, 0).decode('utf-8')
    if message.startswith('{'):
        message = json.loads(message)
        return jsonify(message)
    else:
        return jsonify({'message': message, 'type': 'text'})


@app.route('/last_measurements')
def last_measurements_handler():
    return jsonify({
        'measurements': list(map(lambda x: get_measurement(x, 'Enthalpy'), reversed(get_sensor_data('Bench2', 100))))
    })


@app.route('/last_measurement')
def last_measurement_handler():
    return jsonify({'measurement': get_measurement(get_sensor_data('Bench2')[0], 'Enthalpy')})


@app.route('/talk')
def talk_handler():
    response = analyze_message(request.args.get('message'))
    messages.save_message(redis, 0, json.dumps(response))

    return jsonify({'success': True})


if int(os.environ.get('DEBUG', 1)) == 1:
    app.run(debug=True)
