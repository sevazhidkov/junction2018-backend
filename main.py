import os

from flask import Flask, jsonify, request
from redis import Redis
from measures import measurements

app = Flask(__name__)
redis = Redis(db=1)


@app.route('/')
def main_handler():
    return jsonify({'success': True})


@app.route('/measure')
def measure_handler():
    measurement = request.args.get('name')
    return jsonify({'value': measurements[measurement]()})


if int(os.environ.get('DEBUG', 1)) == 1:
    app.run(debug=True)