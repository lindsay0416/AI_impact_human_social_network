import io
import matplotlib.pyplot as plt
import networkx as nx
from flask import Flask, Response
import pickle

app = Flask(__name__)

@app.route('/graph')
def plot_graph():
    # Load the graph from a pickle file
    with open('../saved/G.pickle', 'rb') as f:
        G = pickle.load(f)

    # Draw the graph
    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw(G, ax=ax, with_labels=True)

    # Save the plot to a BytesIO buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close(fig)
    img_buffer.seek(0)

    # Serve the image
    return Response(img_buffer, mimetype='image/png')

@app.route('/')
def home():
    return '''
        <h1>NetworkX Graph from Pickle</h1>
        <img src="/graph" alt="Graph"/>
    '''

if __name__ == '__main__':
    app.run(debug=True)
