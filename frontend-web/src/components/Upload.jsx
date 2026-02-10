import { useState } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const Upload = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setMessage('');
    };

    const handleUpload = async () => {
        if (!file) {
            setMessage('Please select a file first.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        setLoading(true);
        setMessage('');

        try {
            const response = await axios.post(`${API_BASE_URL}/upload/`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            setMessage('Upload successful!');
            if (response.data && onUploadSuccess) {
                onUploadSuccess(response.data);
            }
        } catch (error) {
            console.error(error);
            setMessage('Upload failed. Please try again or check console for details.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card" style={{ textAlign: 'center' }}>
            <h2>Upload CSV</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', alignItems: 'center' }}>
                <input type="file" accept=".csv" onChange={handleFileChange} />
                <button
                    className="btn btn-primary"
                    onClick={handleUpload}
                    disabled={loading || !file}
                >
                    {loading ? 'Processing...' : 'Upload & Analyze'}
                </button>
            </div>
            {message && (
                <p style={{ marginTop: '1rem', fontSize: '0.9rem', color: message.includes('failed') ? 'var(--error)' : 'var(--success)' }}>
                    {message}
                </p>
            )}
        </div>
    );
};

export default Upload;
