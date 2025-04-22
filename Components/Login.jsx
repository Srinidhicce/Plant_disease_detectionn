// src/components/Login.js
import React from 'react';
import { Link } from 'react-router-dom';
import './LoginSignup.css';

const Login = () => {
  return (
    <div className="box login-box">
      <h2>Login</h2>
      <input type="text" placeholder="Username" />
      <input type="password" placeholder="Password" />
      <button className="primary-btn">Login</button>
      <p className="redirect-text">
        Don't have an account? <Link to="/signup">Create one</Link>
      </p>
    </div>
  );
};

export default Login;
