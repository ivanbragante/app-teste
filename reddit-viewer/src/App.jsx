import React, { useState, useEffect } from 'react';
import PostCard from './components/PostCard';

function App() {
  const [data, setData] = useState({ n8n: [], automation: [] });
  const [activeTab, setActiveTab] = useState('n8n');
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = () => {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    fetch(`${apiUrl}/data?t=` + new Date().getTime())
      .then(res => res.json())
      .then(jsonData => {
        setData(jsonData);
        setLoading(false);
        setRefreshing(false);
      })
      .catch(err => {
        console.error("Error fetching data:", err);
        setLoading(false);
        setRefreshing(false);
      });
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      await fetch(`${apiUrl}/refresh`, { method: 'POST' });
      // Wait a bit for file write to complete
      setTimeout(fetchData, 1000);
    } catch (error) {
      console.error("Error refreshing data:", error);
      setRefreshing(false);
      alert("Failed to refresh data. Is the local server running?");
    }
  };

  if (loading) {
    return <div className="loading">Loading insights...</div>;
  }

  const posts = data[activeTab] || [];

  return (
    <div className="app-container">
      <header className="header">
        <h1 className="title">Reddit Insights</h1>
        <p className="subtitle">Top trending discussions from r/n8n & r/automation</p>
        <button
          onClick={handleRefresh}
          disabled={refreshing}
          className="refresh-btn"
        >
          {refreshing ? '🔄 Refreshing...' : '🔄 Refresh Data'}
        </button>
      </header>

      <div className="tabs">
        <button
          className={`tab-btn n8n ${activeTab === 'n8n' ? 'active' : ''}`}
          onClick={() => setActiveTab('n8n')}
        >
          r/n8n
        </button>
        <button
          className={`tab-btn automation ${activeTab === 'automation' ? 'active' : ''}`}
          onClick={() => setActiveTab('automation')}
        >
          r/automation
        </button>
      </div>

      <main className="grid">
        {posts.map((post, index) => (
          <PostCard key={index} post={post} />
        ))}
      </main>
    </div>
  );
}

export default App;
