import os

from flask import Flask, jsonify, request
from models import UserRegistration
from pydantic import ValidationError

import sqlite3

folder_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(folder_path, 'my_db.db')
app = Flask(__name__)

def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    print("Initializing...")
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT NOT NULL,
                     email TEXT NOT NULL UNIQUE,
                     password TEXT NOT NULL,
                     birth_date TEXT NOT NULL,
                     phone_number TEXT NOT NULL
                     )""")

@app.route('/')
def home():
    return jsonify({"message": "Hello!"})

@app.route('/registration', methods=['POST'])
def user_registration():
    try:
        user = UserRegistration(**request.get_json(silent=True))
    except ValidationError as e:
        return jsonify({"error": e.errors(include_url=False)}), 400

    try:
        with get_db() as conn:
            conn.execute("""INSERT INTO users (username, email, password, birth_date, phone_number)
                            VALUES (?, ?, ?, ?, ?)""", (user.username, user.email,
                                                        user.password, user.birth_date,
                                                        user.phone_number))
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "User with this email already exists"}), 400

    return jsonify({'message': 'User created'}), 201

@app.route('/users')
def users():
    with get_db() as conn:
        data = conn.execute("""SELECT * FROM users""").fetchall()
        return jsonify([dict(row) for row in data]), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

