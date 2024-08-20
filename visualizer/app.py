from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
from flask_socketio import SocketIO, emit
import os
import subprocess
import time

app = Flask(__name__)
app.secret_key = 'secretkey'
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form_data = session.get('parameters', {})
    if not form_data and os.path.exists('input/parameters.json'):
        with open('input/parameters.json', 'r') as json_file:
            form_data = json.load(json_file)
            session['parameters'] = form_data 

    return render_template('simulation.html', data=form_data)

@app.route('/submit', methods=['POST'])
def submit_parameters():
    parameters = {
        "round": request.form.get('round', type=int),
        "timestep": request.form.get('timestep', type=int),
        "influence_prob": request.form.get('influence_prob', type=float),
        "is_directed": request.form.get('is_directed', 'false').lower() == 'true',
        "is_external_dataset": request.form.get('is_external_dataset', 'false').lower() == 'true',
        "node_size": request.form.get('node_size', type=int),
        "random_edges": request.form.get('random_edges', type=int),
        "connect_prob": request.form.get('connect_prob', type=float),
        "evolution_prob": request.form.get('evolution_prob', type=float),
        "generate_user_profile": request.form.get('generate_user_profile', 'false').lower() == 'true',
        "user_profile_prompt": request.form.get('user_profile_prompt', type=str),
        "location": request.form.get('location', type=str),
        "broadcasting_prob": request.form.get('broadcasting_prob', type=float),
        "initial_message": request.form.get('initial_message', type=str)
    }

    os.makedirs('input', exist_ok=True)
    with open('input/parameters.json', 'w') as json_file:
        json.dump(parameters, json_file, indent=4)
    
    session['parameters'] = parameters
    return redirect(url_for('index'))

@app.route('/start-simulation', methods=['POST'])
def start_simulation():
    try:
        script_path = os.path.join(os.path.dirname(__file__),'simulation.py')
        subprocess.run(['python', script_path], check=True)

        return jsonify({"status": "Simulation started and completed successfully."})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "Simulation failed.", "error": str(e)}), 500
    
@app.route('/simulation-result', methods=['GET'])
def get_simulation_result():
    try:
        with open('saved/results.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"status": "No simulation result found."}), 404
    
if __name__ == '__main__':
    app.run(debug=True)