import React, { useState } from 'react'
import './Signup.css'
import { Link } from 'react-router-dom'

import user_icon from '../Assets/person.png'
import password_icon from '../Assets/password.png'
import email_icon from '../Assets/email.png'

export const Signup = () => {

    return (
        <div className='container'>
            <div className='header'>
                <div className="text">Sign Up</div>
                <div className="underline"></div>
            </div>
            <form className="inputs">
                <div className="input">
                    <img src={user_icon} alt="user" />
                    <input type="text" placeholder="Username" />
                </div>
                
                <div className="input">
                    <img src={email_icon} alt="email" />
                    <input type="email" placeholder="Email" />
                </div>
                <div className="input">
                    <img src={password_icon} alt="password" />
                    <input type="password" placeholder="Password" />
                </div>
            </form>
            
            <div className="submit-container">
                <button type='submit' className="submit">Sign Up</button>
                <Link to="/" className="submit gray">Login</Link>
            </div>
        </div>
    )
}
