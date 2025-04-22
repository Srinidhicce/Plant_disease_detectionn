import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        {/* <span>PureHarvest</span> */}
        <img src="/image.png" alt="Logo" className="navbar-logo-img" />
      </div>

      <div className="navbar-links">
        <Link to="/">Home</Link>
        <Link to="/predict">Predict</Link>
        <Link to="/chatbot">Chatbot</Link>
        <Link to="/profile">Profile</Link>
        <Link to="/login">Login</Link>
      </div>
    </nav>
  );
}

export default Navbar;
