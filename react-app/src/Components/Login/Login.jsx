import React, { useState } from 'react'
import './Login.css'
import { Link } from 'react-router-dom'
import { validationLogin } from '../Utils/Validation'

import password_icon from '../Assets/password.png'
import email_icon from '../Assets/email.png'

export const Login = () => {
    const [values, setValues] = useState({
        email: '',
        password: ''
    })

    const [errors, setErrors] = useState({})

    const handleInput = (e) => {
        setValues(prev => ({...prev, [e.target.name]: e.target.value}))
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        setErrors(validationLogin(values))
    }

    return (
        <div className='container'>
            <div className='header'>
                <div className="text">Login</div>
                <div className="underline"></div>
            </div>
            <form className="inputs" onSubmit={handleSubmit}>              
                <div className="input">
                    <img src={email_icon} alt="email" />
                    <input type="email" placeholder="Email" onChange={handleInput} name="email" />
                    {errors.email && <span className="error">{errors.email}</span>}
                </div>
                <div className="input">
                    <img src={password_icon} alt="password" />
                    <input type="password" placeholder="Password" onChange={handleInput} name="password" />
                    {errors.password && <span className="error">{errors.password}</span>}
                </div>
            </form>
            <div className="remember-forgot">
                <label><input type="checkbox" />Remember me</label>
                <div className="forgot">Lost Password ? <span>Click Here !</span></div>
            </div>
            
            <div className="submit-container">
                <Link to="/signup" className="submit gray">Sign Up</Link>
                <div className="submit">Login</div>
            </div>
        </div>
    )
}
