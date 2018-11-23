import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def main():
    return jsonify({'success': True})


if int(os.environ.get('DEBUG', 1)) == 1:
    app.run(debug=True)
else:
    app.run('0.0.0.0', 6969)
