import React, { useState } from 'react'
import './Login.css'
import { Link, useNavigate } from 'react-router-dom'
import validationLogin from '../Utils/ValidationLogin';  // No curly braces for default export
import axios from 'axios'


import password_icon from '../Assets/password.png'
import email_icon from '../Assets/email.png'

export const Login = () => {
    const [values, setValues] = useState({
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
        setErrors(validationLogin(values));
        if (errors.email === '' && errors.password === '') {
            axios.post('http://localhost:8081/login', values)
            .then(res => {
                console.log(res);
                if (res.data === 'Success') {
                    console.log('Login Success');
                    navigation('/home');
                } else {
                    console.log('Login Failed');
                    alert('Login Failed');
                }
            })
            .catch(err => {
                console.log(err);
            })
        }
    }

    return (
        <div className='container'>
            <div className='header'>
                <div className="text">Login</div>
                <div className="underline"></div>
            </div>
            <form action="" onSubmit={handleSubmit}>
                <div className="inputs">
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
                <div className="remember-forgot">
                    <label><input type="checkbox" />Remember me</label>
                    <div className="forgot">Lost Password ? <span>Click Here !</span></div>
                </div>
                
                <div className="submit-container">
                    <Link to="/signup" className="submit gray">Sign Up</Link>
                    <button type='submit' className="submit">Login</button>
                </div>
            </form>
        </div>
    )
}
