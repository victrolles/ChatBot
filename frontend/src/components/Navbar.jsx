import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext';

import chatbot_logo from '../assets/logo.png'

const Navbar = () => {

    const { logout } = useAuth()
    const navigate = useNavigate()

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
                <span>John</span>
                <button onClick={handleLogout}>Logout</button>
            </div>
        </div>
    )
}

export default Navbar