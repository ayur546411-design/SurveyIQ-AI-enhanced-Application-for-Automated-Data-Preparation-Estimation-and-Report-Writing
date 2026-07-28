import React from 'react';
import Layout from './components/layout/Layout';
import Button from './components/common/Button';
import './App.css';

function App() {
  return (
    <Layout>
      <div className="dashboard-content">
        <h1>Welcome to SurveyIQ</h1>
        <p>Your one-stop solution for automated data preparation, estimation, and report writing.</p>
        
        <div style={{ marginTop: '2rem' }}>
          <h2>Quick Actions</h2>
          <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
            <Button variant="primary" onClick={() => alert('New Survey')}>Create New Survey</Button>
            <Button variant="secondary" onClick={() => alert('View Reports')}>View Reports</Button>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default App;
