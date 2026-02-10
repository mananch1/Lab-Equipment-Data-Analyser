# API Routes Documentation

The backend provides a REST API built with Django REST Framework.

## Base URL
Local: `http://localhost:8000/api/`
Production: `https://lab-equipment-data-analyser-backend.onrender.com/api/`

## Endpoints

### 1. Upload Dataset
Uploads a CSV file containing equipment data for analysis.

- **URL**: `/upload/`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: The CSV file to upload (Required).

**Expected CSV Columns:**
- `Equipment Name`
- `Type`
- `Flowrate`
- `Pressure`
- `Temperature`

**Success Response (201 Created):**
```json
{
    "id": 1,
    "file": "/media/uploads/data.csv",
    "uploaded_at": "2023-10-27T10:00:00Z",
    "summary": {
        "total_count": 100,
        "averages": {
            "Flowrate": 50.5,
            "Pressure": 10.2,
            "Temperature": 98.6
        },
        "type_distribution": {
            "Pump": 40,
            "Valve": 60
        },
        "averages_by_type": {
            "Pump": { "Flowrate": 60.0, ... },
            "Valve": { "Flowrate": 40.0, ... }
        },
        "preview": [ ... ]
    }
}
```

### 2. Get History
Retrieves the last 5 uploaded datasets with their analysis summaries.

- **URL**: `/history/`
- **Method**: `GET`

**Success Response (200 OK):**
```json
[
    {
        "id": 1,
        "file": "...",
        "uploaded_at": "...",
        "summary": { ... }
    },
    ...
]
```
