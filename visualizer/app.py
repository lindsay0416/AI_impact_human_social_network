from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('log', {'msg': 'Welcome! Waiting for news to propagate...'})

@socketio.on('share_news')
def handle_share_news(data):
    print(f"News received: {data['msg']}")
    # Simulate the propagation probability
    if random.random() < 0.5:  # 50% chance to propagate the news
        emit('news', {'msg': data['msg']}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
