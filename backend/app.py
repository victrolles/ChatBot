from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import bcrypt
import mysql.connector
from mysql.connector import Error
from bot import Bot
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # More permissive CORS
# CORS(app)

chatBot = Bot()

def init_db():
    """Initialize the database schema."""
    try:
        connection = mysql.connector.connect(
            host="mysql",
            user="root",
            password="password"
        )
        cursor = connection.cursor()

        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS chatbot_db")
        cursor.execute("USE chatbot_db")

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        """)

        # Create chats table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                id_user INT NOT NULL,
                FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_chat INT NOT NULL,
                content TEXT NOT NULL,
                bot BOOLEAN NOT NULL,
                date DATETIME NOT NULL,
                FOREIGN KEY (id_chat) REFERENCES chats(id) ON DELETE CASCADE
            );
        """)

        connection.commit()
        print("Database initialized successfully.")
    except Error as e:
        print(f"Database initialization failed: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def get_db_connection():
    """Get a database connection."""
    try:
        # connection = mysql.connector.connect(
        #     host=os.environ.get('MYSQL_HOST', 'mysql'),
        #     user=os.environ.get('MYSQL_USER', 'root'),
        #     password=os.environ.get('MYSQL_PASSWORD', 'password'),
        #     database=os.environ.get('MYSQL_DATABASE', 'chatbot_db')
        # )
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="chatbot_db",
            port=3306
        )
        
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise

@app.route('/signup', methods=['POST'])
def signup():
    """Handle user signup with password hashing."""
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, hashed_password.decode('utf-8')))
        connection.commit()
        return jsonify("User created successfully"), 201
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify("Error"), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/login', methods=['POST'])
def login():
    """Handle user login with password verification."""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify("Success"), 200
        else:
            return jsonify("Failed"), 401
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify("Error"), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/createChat', methods=['POST'])
def create_chat():
    """Create a new chat for a user."""
    data = request.json
    email = data.get('email')
    content = data.get('content')

    chat_name = chatBot.get_chat_name(content)

    print(f"Chat name: {chat_name}")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "INSERT INTO chats (name, id_user) VALUES (%s, (SELECT id FROM users WHERE email = %s));"
        cursor.execute(query, (chat_name, email))
        connection.commit()

        # Fetch the newly created chat
        query = "SELECT * FROM chats WHERE name = %s;"
        cursor.execute(query, (chat_name,))
        new_chat = cursor.fetchone()

        print(f"New chat: {new_chat}")

        return jsonify(new_chat), 200
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify("Error"), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/sendMessage', methods=['POST'])
def send_message():
    """Handle sending a message and getting a bot response."""
    data = request.json
    chat_id = data.get('chatId')
    user_message = data.get('content')
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        # Fetch conversation context
        query = "SELECT id, content, bot FROM messages WHERE id_chat = %s ORDER BY date ASC"
        cursor.execute(query, (chat_id,))
        messages = cursor.fetchall()

        formatted_messages = [
            (msg['id'], msg['content'], None, None, 1 if msg['bot'] else 0)
            for msg in messages
        ]

        # Get bot response
        bot_response = chatBot.get_response(formatted_messages, user_message)
        print(f"Bot response length: {len(bot_response)}")

        # Store user message
        query_user = "INSERT INTO messages (id_chat, content, bot, date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_user, (chat_id, user_message, False, date))

        # Store bot response
        query_bot = "INSERT INTO messages (id_chat, content, bot, date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_bot, (chat_id, bot_response, True, date))

        connection.commit()
        return jsonify({"response": bot_response}), 200
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify("Error"), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/getChatsFromUser', methods=['POST'])
def getChatsFromUser():
    data = request.json
    email = data.get('name')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT \
                    CHT.name AS 'chatName',\
                    CHT.id AS 'chatId',\
                    MSG.content AS 'lastMessage'\
                FROM \
                    chats CHT\
                INNER JOIN \
                    messages MSG \
                ON \
                    CHT.id = MSG.id_chat\
                WHERE \
                    MSG.id = (\
                        SELECT MAX(MSG2.id)\
                        FROM messages MSG2\
                        WHERE MSG2.id_chat = CHT.id\
                    )\
                AND \
                    CHT.id_user = (\
                        SELECT USR.id \
                        FROM users USR \
                        WHERE USR.email = %s\
                    );\
"
        # print(query)
        cursor.execute(query, (email,))
        chats = cursor.fetchall()
        if chats:
            return jsonify(chats), 200
        else:
            return jsonify({"message": "No chats found"}), 404
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify("Error"), 500
    finally:
        cursor.close()

@app.route('/getUsernameFromMail', methods=['POST'])
def getUsernameFromMail():
    data = request.json
    email = data.get('email')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT \
                    USR.username AS 'username'\
                FROM \
                    users USR\
                WHERE \
                    USR.email = %s\
                ;"
        
        cursor.execute(query, (email,))
        username = cursor.fetchone()
        if username:
            return jsonify(username), 200
        else:
            return jsonify({"message": "No username found"}), 404
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify("Error"), 500
    finally:
        cursor.close()

@app.route('/getMessagesFromChat', methods=['POST'])
def getMessagesFromChat():
    data = request.json
    chatId = data.get('chatId')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT \
                    *\
                FROM \
                    messages MSG\
                WHERE \
                    MSG.id_chat = %s\
                ;"
        
        cursor.execute(query, (chatId,))
        messages = cursor.fetchall()
        if messages:
            return jsonify(messages), 200
        else:
            return jsonify({"message": "No messages found"}), 404
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify("Error"), 500
    finally:
        cursor.close()

if __name__ == '__main__':
    # init_db()
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000)
