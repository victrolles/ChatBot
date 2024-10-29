const express = require('express');
const mysql = require('mysql');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'chatbot_db'
});

app.post('/signup', (req, res) => {
    const { username, email, password } = req.body;
    const query = `INSERT INTO users (username, email, password) VALUES ('${username}', '${email}', '${password}')`;
    db.query(query, (err, data) => {
        if (err) {
            return res.json("Error");
        }
        return res.json(data);
    });
});

app.post('/login', (req, res) => {
    const { email, password } = req.body;
    const query = `SELECT * FROM users WHERE email = '${email}' AND password = '${password}'`;
    db.query(query, (err, data) => {
        if (err) {
            return res.json("Error");
        }
        if (data.length > 0) {
            return res.json("Success");
        } else {
            return res.json("Failed");
        }
    });
});

app.listen(8081, () => {
    console.log('Server is running on port 8081');
});