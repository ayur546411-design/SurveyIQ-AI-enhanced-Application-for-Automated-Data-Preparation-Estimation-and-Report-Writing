import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-logo">
        <h2>SurveyIQ</h2>
      </div>
      <nav className="header-nav">
        <ul>
          <li><a href="#dashboard">Dashboard</a></li>
          <li><a href="#reports">Reports</a></li>
          <li><a href="#settings">Settings</a></li>
        </ul>
      </nav>
      <div className="header-profile">
        <span>User Profile</span>
      </div>
    </header>
  );
};

export default Header;
