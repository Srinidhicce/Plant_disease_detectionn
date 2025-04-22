// src/components/Signup.js
import React from 'react';
import { Link } from 'react-router-dom';
import './LoginSignup.css';

const Signup = () => {
  return (
    <div className="box signup-box">
      <h2>Signup</h2>
      <input type="text" placeholder="Username" />
      <input type="email" placeholder="Email" />
      <input type="password" placeholder="Password" />
      <button className="primary-btn">Signup</button>
      <p className="redirect-text">
        Already have an account? <Link to="/login">Log in</Link>
      </p>
    </div>
  );
};

export default Signup;
