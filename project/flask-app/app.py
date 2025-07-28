from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        data = request.get_json()
        cur.execute("INSERT INTO messages (content) VALUES (%s)", (data['content'],))
        conn.commit()
        return jsonify({"status": "Message stored"}), 201
    else:
        cur.execute("SELECT * FROM messages")
        messages = cur.fetchall()
        return jsonify(messages)

@app.route('/')
def home():
    return 'Welcome to the Stateful Flask App!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
