import { useState } from 'react';
import Upload from './components/Upload';
import Dashboard from './components/Dashboard';
import History from './components/History';
import './App.css';

function App() {
  const [currentData, setCurrentData] = useState(null);

  return (
    <div className="app-container">
      <header>
        <h1>Chemical Equipment Visualizer</h1>
        <p>Your one stop shop for Analytics & Parameter Visualization</p>
      </header>

      <div className="main-content">
        <div className="left-panel">
          <Upload onUploadSuccess={setCurrentData} />
          <History onSelectDataset={setCurrentData} />
        </div>

        <div className="right-panel card">
          {currentData ? (
            <Dashboard data={currentData} />
          ) : (
            <div style={{ textAlign: 'center', padding: '4rem 2rem', color: 'var(--text-secondary)' }}>
              <p style={{ fontSize: '1.1rem', marginBottom: '1rem' }}>No Data Selected</p>
              <p style={{ fontSize: '0.9rem' }}>Upload a CSV file or select a past dataset from history to view analytics.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
