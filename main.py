import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def main():
    return jsonify({'success': True})


if os.environ.get('DEBUG', True):
    app.run(debug=True)
else:
    app.run('0.0.0.0', 8080)
