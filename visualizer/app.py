from flask import Flask, jsonify, send_from_directory
import json

app = Flask(__name__)

@app.route('/results')
def get_results():
    try:
        with open('saved/results.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify([]), 404

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
