# Chemical Equipment Parameter Visualizer

A modern, hybrid web and desktop application for analyzing and visualizing chemical equipment data.

## Features
- **CSV Upload**: Inspect and analyze equipment data files.
- **Analytics Dashboard**:
  - Real-time calculation of averages and distribution.
  - Interactive charts (Bar & Pie) with "Deep Ocean" aesthetic.
  - **Category Filtering**: Drill down averages by equipment type.
- **History**: Tracks past uploads for quick access.
- **Multi-Platform**:
  - **Web**: React (Vite) + Chart.js with responsive Glassmorphism UI.
  - **Desktop**: Python (PyQt5) + Matplotlib for local usage.
  - **Backend**: Django REST Framework + Pandas for robust data processing.

## Quick Start

### 1. Backend Setup (Django)
```bash
# navigate to backend
cd backend
# Create/Activate Virtual Environment
python -m venv venv
..\venv\Scripts\activate  # Windows
# Install Dependencies
pip install -r requirements.txt
# Run Migrations
python manage.py migrate
# Start Server (Accessible on LAN)
python manage.py runserver 0.0.0.0:8000
```

### 2. Web Frontend (React)
```bash
cd frontend-web
npm install
npm run dev -- --host
```
Access via `http://localhost:5173` or your local IP (e.g., `http://192.168.x.x:5173`) for mobile testing.

### 3. Desktop App (PyQt5)
Ensure backend is running, then:
```bash
cd frontend-desktop
..\venv\Scripts\python.exe main.py
```

## Deployment
See [deployment.md](deployment.md) for detailed instructions on deploying the Backend to **Render** and Frontend to **Vercel**.

## Mobile Access
To access the app from your phone:
1. Ensure your computer and phone are on the same Wi-Fi.
2. Run backend with `0.0.0.0:8000`.
3. Update `frontend-web/src/config.js` with your computer's IP.
4. Open the frontend URL (e.g., `http://192.168.0.103:5173`) on your phone.

## Sample Data
Use `sample_equipment_data.csv` located in the root directory for testing.
