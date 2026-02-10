# Project Setup Guide

This guide provides detailed instructions for setting up the Backend, Web Frontend, and Desktop Application.

## Prerequisites
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **Git**

---

## 1. Backend Setup (Django)

The backend is built with Django REST Framework.

### Steps
1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    - **Windows:**
        ```bash
        ..\venv\Scripts\activate
        ```
    - **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Start the Server:**
    To make the server accessible on your local network (for mobile testing), run:
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```
    Otherwise, for local only:
    ```bash
    python manage.py runserver
    ```

---

## 2. Web Frontend (React)

The web frontend is built with React and Vite.

### Steps
1.  **Navigate to the frontend-web directory:**
    ```bash
    cd frontend-web
    ```

2.  **Install Dependencies:**
    ```bash
    npm install
    ```

3.  **Run Development Server:**
    ```bash
    npm run dev -- --host
    ```

4.  **Access the App:**
    - Local: `http://localhost:5173`
    - Network (Mobile): Check the terminal output for your IP address (e.g., `http://192.168.x.x:5173`).

---

## 3. Desktop App (PyQt5)

The desktop application provides a native experience using Python and PyQt5.

### Steps
1.  **Ensure the Backend is Running:**
    The desktop app communicates with the backend, so make sure step 1 is completed and the server is running.

2.  **Navigate to the frontend-desktop directory:**
    ```bash
    cd frontend-desktop
    ```

3.  **Run the Application:**
    Use the python executable from your backend virtual environment (or create a new one if preferred):
    ```bash
    ..\backend\venv\Scripts\python.exe main.py
    ```

---

## Mobile Access Configuration

To access the web application from your mobile device:
1.  Ensure your computer and phone are connected to the **same Wi-Fi network**.
2.  Run the backend with `0.0.0.0:8000`.
3.  Update `frontend-web/src/config.js` (if hardcoded) with your computer's local IP address.
4.  Open the URL shown in the `npm run dev -- --host` output on your phone.

---

## Verification
To verify the backend API is working correctly without the frontend, you can use the provided Python script:

```bash
# From the root directory
python backend/verify_backend.py
```
This script attempts to upload a dummy dataset and fetch the history, printing the results to the console.
