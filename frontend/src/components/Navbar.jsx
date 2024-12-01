import { React, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

import chatbot_logo from '../assets/logo.png'

const Navbar = () => {

    const [username, setUsername] = useState(null)
    
    const { user, logout } = useAuth()
    const navigate = useNavigate()

    useEffect(() => {
        if (user) {
            axios.post('http://localhost:5000/getUsernameFromMail', { email: user.name })
                .then(res => {
                    if (res.status === 200) {
                        setUsername(res.data.username);  // Store the chats in the state
                        console.log('Username retrieved:', res.data);
                    } else {
                        console.log('No username found for :', user.name);
                    }
                })
                .catch(err => console.error('Error fetching username:', err));
        }
    }, [user]);

    const handleLogout = () => {
        logout()
        navigate('/')
    }

    return (
        <div className='navbar'>
            <div className="logo">
                <img src={chatbot_logo} alt="chatbot_logo" />
            </div>
            <div className="user">
                <span>{username}</span>
                <button onClick={handleLogout}>Logout</button>
            </div>
        </div>
    )
}

export default Navbar