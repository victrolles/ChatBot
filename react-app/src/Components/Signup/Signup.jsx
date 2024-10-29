import React, { useState } from 'react'
import './Signup.css'
import { Link, useNavigate } from 'react-router-dom'

import validationSignup from '../Utils/ValidationSignup';
import axios from 'axios'

import user_icon from '../Assets/person.png'
import password_icon from '../Assets/password.png'
import email_icon from '../Assets/email.png'

export const Signup = () => {

    const [values, setValues] = useState({
        username: '',
        email: '',
        password: ''
    })

    const navigation = useNavigate();

    const [errors, setErrors] = useState({})

    const handleInput = (e) => {
        setValues(prev => ({...prev, [e.target.name]: e.target.value}))
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        setErrors(validationSignup(values));
        if (errors.username === '' && errors.email === '' && errors.password === '') {
            axios.post('http://localhost:8081/signup', values)
            .then(res => {
                console.log(res);
                navigation('/');
            })
            .catch(err => {
                console.log(err);
            })
        }
    }

    return (
        <div className='container'>
            <div className='header'>
                <div className="text">Sign Up</div>
                <div className="underline"></div>
            </div>
            <form action="" onSubmit={handleSubmit}>
                <div className="inputs">
                    <div className="input-container">
                        <div className="input">
                            <img src={user_icon} alt="username" />
                            <input type="text" placeholder="Username" onChange={handleInput} name="username" />
                        </div>
                        {errors.username && <span className="error">{errors.username}</span>}
                    </div>  
                    <div className="input-container">
                        <div className="input">
                            <img src={email_icon} alt="email" />
                            <input type="email" placeholder="Email" onChange={handleInput} name="email" />
                        </div>
                        {errors.email && <span className="error">{errors.email}</span>}
                    </div>            
                    <div className="input-container">
                        <div className="input">
                            <img src={password_icon} alt="password" />
                            <input type="password" placeholder="Password" onChange={handleInput} name="password" />
                        </div>
                        {errors.password && <span className="error">{errors.password}</span>}
                    </div>
                </div>
                
                <div className="submit-container">
                    <button type='submit' className="submit">Sign Up</button>
                    <Link to="/" className="submit gray">Login</Link>
                </div>
            </form>
        </div>
    )
}
