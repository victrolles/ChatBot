from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatbot_db"
)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    cursor = db.cursor()
    try:
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, password))
        db.commit()
        return jsonify("User created successfully"), 201
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify("Error"), 500
    finally:
        cursor.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        if user:
            return jsonify("Success"), 200
        else:
            return jsonify("Failed"), 401
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify("Error"), 500
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(port=8081, debug=True)
