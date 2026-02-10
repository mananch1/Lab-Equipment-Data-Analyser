import { useEffect, useState } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const History = ({ onSelectDataset }) => {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const response = await axios.get(`${API_BASE_URL}/history/`);
                setHistory(response.data);
            } catch (error) {
                console.error("Failed to fetch history", error);
            }
        };

        fetchHistory();
        // Poll every 5 seconds to keep history updated
        const interval = setInterval(fetchHistory, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="card">
            <h3>History (Last 5 Uploads)</h3>
            {history.length === 0 ? <p className="text-secondary">No history yet.</p> : (
                <ul className="history-list">
                    {history.map((item) => (
                        <li key={item.id}
                            className="history-item"
                            onClick={() => onSelectDataset(item)}
                        >
                            <div style={{ fontWeight: '500' }}>{new Date(item.uploaded_at).toLocaleString()}</div>
                            <div className="history-meta">
                                Records: {item.summary?.total_count || 'N/A'}
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default History;
