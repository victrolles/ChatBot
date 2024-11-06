from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

from bot import Bot

app = Flask(__name__)
CORS(app)

chatBot = Bot()

# Database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatbot_db",
    port=3306
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

@app.route('/getChatsFromUser', methods=['POST'])
def getChatsFromUser():
    data = request.json
    email = data.get('name')

    cursor = db.cursor(dictionary=True)
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

    cursor = db.cursor(dictionary=True)
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

    cursor = db.cursor(dictionary=True)
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

@app.route('/sendMessage', methods=['POST'])
def sendMessage():
    data = request.json
    chatId = data.get('chatId')
    content = data.get('content')
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor = db.cursor()

    try:
        # Get all conversations from the chat
        query = "SELECT * FROM messages WHERE id_chat = %s;"
        cursor.execute(query, (chatId,))
        messages = cursor.fetchall()
        print(messages)
        
        # Bot response
        bot_response = chatBot.get_response(messages, content)
        
        # Send back to the database
        query1 = "INSERT INTO messages (id_chat, content, bot, date) VALUES (%s, %s, %s, %s);"
        cursor.execute(query1, (chatId, content, False, date))
        
        query2 = "INSERT INTO messages (id_chat, content, bot, date) VALUES (%s, %s, %s, %s);"
        cursor.execute(query2, (chatId, bot_response, True, date))
        
        db.commit()

        return jsonify("Message sent successfully"), 200
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify("Error"), 500
    finally:
        cursor.close()

@app.route('/createChat', methods=['POST'])
def createChat():

    # Get the email and content from the request
    data = request.json
    email = data.get('email')
    content = data.get('content')

    # Ask the chatbot to create a chat name
    chatName = chatBot.get_chat_name(content)
    # chatName = content

    # Add the chat to the database
    cursor = db.cursor(dictionary=True)
    try:

        query = "INSERT INTO chats (name, id_user) VALUES (%s, (SELECT id FROM users WHERE email = %s));"

        cursor.execute(query, (chatName, email))
        db.commit()

        query = "SELECT * FROM chats CHT WHERE CHT.name = %s;"
        cursor.execute(query, (chatName,))
        newChat = cursor.fetchone()

        return jsonify(newChat), 200
    
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify("Error"), 500
    
    finally:
        cursor.close()

    

if __name__ == '__main__':
    app.run(port=8081, debug=True)
