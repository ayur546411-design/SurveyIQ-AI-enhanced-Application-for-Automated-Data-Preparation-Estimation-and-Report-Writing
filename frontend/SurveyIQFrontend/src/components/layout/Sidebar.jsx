import React from 'react';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        <ul>
          <li><a href="#overview">Overview</a></li>
          <li><a href="#analytics">Analytics</a></li>
          <li><a href="#surveys">Surveys</a></li>
          <li><a href="#audiences">Audiences</a></li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
