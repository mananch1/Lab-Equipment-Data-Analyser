import React from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const Dashboard = ({ data }) => {
    if (!data || !data.summary) return <p>No data to display. Please upload a CSV file.</p>;

    const { summary } = data;
    const { averages, type_distribution, total_count, averages_by_type } = summary;

    // State for filter
    const [selectedType, setSelectedType] = React.useState('All');

    // Determine data to show based on selection
    let displayAverages = averages;
    if (selectedType !== 'All' && averages_by_type && averages_by_type[selectedType]) {
        displayAverages = averages_by_type[selectedType];
    }

    const barData = {
        labels: Object.keys(displayAverages),
        datasets: [
            {
                label: selectedType === 'All' ? 'Average Values (All)' : `Average Values (${selectedType})`,
                data: Object.values(displayAverages),
                backgroundColor: 'rgba(6, 182, 212, 0.2)', // Cyan-500 low opacity
                borderColor: '#22d3ee', // Cyan-400
                borderWidth: 2,
                borderRadius: 8,
                hoverBackgroundColor: 'rgba(6, 182, 212, 0.4)',
            },
        ],
    };

    const pieData = {
        labels: Object.keys(type_distribution),
        datasets: [
            {
                data: Object.values(type_distribution),
                backgroundColor: [
                    '#818cf8', // Indigo
                    '#34d399', // Emerald
                    '#f472b6', // Pink
                    '#fbbf24', // Amber
                    '#22d3ee', // Cyan
                ],
                borderColor: '#1e293b', // Match card bg somewhat
                borderWidth: 2,
                hoverOffset: 15,
            },
        ],
    };

    return (
        <div>
            <div className="dashboard-header">
                <div>
                    <h2 style={{ marginBottom: '0.5rem', color: '#f1f5f9' }}>Analytics Dashboard</h2>
                    <p style={{ color: 'var(--text-secondary)', margin: 0 }}>Real-time equipment parameter analysis</p>
                </div>
                <div className="stat-card">
                    <span className="stat-label">Total Records</span>
                    <div className="stat-value">{total_count}</div>
                </div>
            </div>

            <div className="stats-grid">
                <div className="card" style={{ height: '400px', marginBottom: 0 }}>
                    <div className="chart-header">
                        <h3 style={{ margin: 0 }}>Average Parameters</h3>
                        <div style={{ position: 'relative' }}>
                            <select
                                value={selectedType}
                                onChange={(e) => setSelectedType(e.target.value)}
                                style={{
                                    padding: '5px 10px',
                                    borderRadius: '6px',
                                    border: '1px solid var(--border-color)',
                                    background: 'rgba(30, 41, 59, 0.6)',
                                    color: '#f0f9ff',
                                    cursor: 'pointer',
                                    fontSize: '0.9rem',
                                    outline: 'none'
                                }}
                            >
                                <option value="All">All Types</option>
                                {Object.keys(type_distribution).map(type => (
                                    <option key={type} value={type}>{type}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                    <div style={{ height: '300px', position: 'relative', width: '100%' }}>
                        <Bar
                            data={barData}
                            options={{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {
                                    legend: { display: false },
                                    tooltip: {
                                        backgroundColor: 'rgba(30, 41, 59, 0.95)',
                                        titleColor: '#f8fafc',
                                        bodyColor: '#e2e8f0',
                                        borderColor: 'rgba(255,255,255,0.1)',
                                        borderWidth: 1
                                    }
                                },
                                scales: {
                                    y: {
                                        beginAtZero: true,
                                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                        ticks: { color: '#cbd5e1' }
                                    },
                                    x: {
                                        grid: { display: false },
                                        ticks: { color: '#cbd5e1' }
                                    }
                                }
                            }}
                        />
                    </div>
                </div>
                <div className="card" style={{ height: '400px', marginBottom: 0 }}>
                    <h3>Equipment Type Distribution</h3>
                    <div style={{ height: '320px', display: 'flex', justifyContent: 'center', position: 'relative', width: '100%' }}>
                        <Pie
                            data={pieData}
                            options={{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {
                                    legend: {
                                        position: 'right',
                                        labels: { color: '#f1f5f9' }
                                    }
                                }
                            }}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
