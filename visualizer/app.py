from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['form_data'] = request.form
        return redirect(url_for('index'))
    form_data = session.get('form_data', {})
    return render_template('simulation.html', data=form_data)

@app.route('/submit', methods=['POST'])
def submit_parameters():
    # Read the form data
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

    # Write to JSON file
    os.makedirs('input', exist_ok=True)
    with open('input/parameters.json', 'w') as json_file:
        json.dump(parameters, json_file, indent=4)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
