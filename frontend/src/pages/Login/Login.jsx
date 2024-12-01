import React, { useState } from 'react';
import './Login.css';
import { Link, useNavigate } from 'react-router-dom';
import validationLogin from '../../utils/ValidationLogin';  // No curly braces for default export
import axios from 'axios'
import { useAuth } from '../../context/AuthContext';

import password_icon from '../../assets/password.png';
import email_icon from '../../assets/email.png';

export const Login = () => {
    const [values, setValues] = useState({
        email: '',
        password: ''
    })

    const { login } = useAuth();

    const navigation = useNavigate();

    const [errors, setErrors] = useState({})

    const handleInput = (e) => {
        setValues(prev => ({...prev, [e.target.name]: e.target.value}))
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        const validationErrors = validationLogin(values);
        setErrors(validationErrors);
    
        if (!validationErrors.email && !validationErrors.password) {
            console.log('Form submitted');
            try {
                const res = await axios.post('http://localhost:5000/login', values);
                console.log("Login submitted", res);
    
                if (res.data === 'Success') {
                    console.log('Login Success');
                    const userData = { name: values.email };
                    login(userData);
                    navigation('/home');
                } else {
                    console.log('Login Failed');
                    alert('Login Failed');
                }
            } catch (err) {
                console.error(err);
            }
        }
    };

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
