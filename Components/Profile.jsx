// src/components/Profile.js
import React from 'react';
import './LoginSignup.css';

const Profile = () => {
  return (
    <div className="box profile-box">
      <h2>Profile</h2>
      <label>User ID:</label>
      <input type="text" value="user123" readOnly />
      <label>Username:</label>
      <input type="text" defaultValue="John Doe" />
      <div className="button-group">
        <button className="primary-btn">Update</button>
        <button className="danger-btn">Delete Account</button>
      </div>
    </div>
  );
};

export default Profile;
