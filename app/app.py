from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import psycopg2
from prometheus_client import Counter, Histogram
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
socketio = SocketIO(app)

# Prometheus metrics
MESSAGE_COUNTER = Counter('chat_messages_total', 'Total number of chat messages')
MESSAGE_LATENCY = Histogram('message_processing_seconds', 'Time spent processing messages')

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('DB_NAME', 'chatdb'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres')
    )

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
@MESSAGE_LATENCY.time()
def handle_message(data):
    username = data.get('username')
    message = data.get('message')
    
    if username and message:
        # Store message in database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO messages (username, message) VALUES (%s, %s)',
            (username, message)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        # Increment message counter
        MESSAGE_COUNTER.inc()
        
        # Broadcast message to all clients
        emit('new_message', {
            'username': username,
            'message': message
        }, broadcast=True)

if __name__ == '__main__':
    # Create database table if it doesn't exist
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
    
    socketio.run(app, host='0.0.0.0', port=5000) 