# Algorithm Complexity Visualizer

A Flask-based API that analyzes and visualizes the time complexity of various algorithms with **SQLAlchemy database integration**. This tool measures execution times across different input sizes, generates visual graphs, and automatically saves analysis results to a MySQL database.

  
## Features

- **Algorithm Analysis**: Measure time complexity of Bubble Sort, Linear Search, Binary Search, and Nested Loops
- **Visual Graphs**: Generate matplotlib graphs showing performance across input sizes
- **Base64 Encoding**: Graphs returned as base64-encoded images for easy embedding
- **File Storage**: Automatically save graphs to local filesystem
- **Database Integration**: Store all analysis results in MySQL database with SQLAlchemy
- **History Tracking**: Retrieve past analysis results via API endpoints
- **REST API**: Simple HTTP endpoints for all operations

## Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup MySQL Database
```bash
# Start MySQL/XAMPP, then create database
mysql -u root -p
CREATE DATABASE alchemy;
exit;
```

### 3. Run the Application
```bash
python app.py
```

Visit: `http://localhost:3000/analyze?algo=bubble&n=1000&steps=10`

## Table of Contents
- [Installation](#installation)
- [Database Setup](#database-setup)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

  
## Installation

### Prerequisites
- Python 3.x installed on your system

### Step 1: Create a Virtual Environment

In project directory, create a virtual environment:

```bash
python -m venv .venv
```

### Step 2: Activate the Virtual Environment

**On Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
.\.venv\Scripts\activate.bat
```

**On Linux/Mac:**
```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

**Or install manually:**
```bash
pip install flask numpy matplotlib sqlalchemy pymysql
```

### Step 4: Verify Installation

Verify that dependencies are installed correctly:

```bash
pip show flask sqlalchemy
```

---

## Database Setup

### 1. Configure Database Connection

Update database credentials in `sqlachemy.py.py`:

```python
DB_USER = 'root'
DB_PASSWORD = ''  # Your MySQL password
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'alchemy'
```

### 2. Create Database

**Option A: Using MySQL Command Line**
```bash
mysql -u root -p
CREATE DATABASE alchemy;
exit;
```

**Option B: Using SQL Script**
```bash
mysql -u root -p < create_database.sql
```

### 3. Initialize Tables

Tables are automatically created when you first run the application. Or manually initialize:

```bash
python sqlachemy.py.py
```

### Database Schema

**Table: `algorithm_analysis`**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Auto-increment primary key |
| algo | VARCHAR(100) | Algorithm name (e.g., "Bubble Sort") |
| items | INTEGER | Number of items processed |
| steps | INTEGER | Step increment used |
| start_time | BIGINT | Start timestamp (milliseconds) |
| end_time | BIGINT | End timestamp (milliseconds) |
| total_time_ms | INTEGER | Total execution time (milliseconds) |
| time_complexity | VARCHAR(50) | Complexity notation (e.g., "O(n²)") |
| path_to_graph | VARCHAR(500) | Path to saved graph image |
| created_at | VARCHAR(50) | Creation timestamp |

---

---

## API Endpoints

### Base URL
```
http://localhost:3000
```

### 1. Home - GET `/`

Returns API information and available algorithms.

**Response:**
```json
{
  "available_algorithms": ["bubble", "linear", "binary", "nested"],
  "example": "/analyze?algo=bubble&n=1000&steps=10"
}
```

### 2. Analyze Algorithm - GET `/analyze`

Analyzes algorithm time complexity and **automatically saves to database**.

**Parameters:**
- `algo` (required): Algorithm name (`bubble`, `linear`, `binary`, `nested`)
- `n` (required): Maximum input size (positive integer)
- `steps` (required): Step increment (positive integer)

**Example:**
```bash
GET http://localhost:3000/analyze?algo=bubble&n=1000&steps=10
```

**Response:**
```json
{
  "algo": "Bubble Sort",
  "items": "1000",
  "steps": "10",
  "start_time": 1738627200000,
  "end_time": 1738627203000,
  "total_time_ms": 3000,
  "time_complexity": "O(n²)",
  "data_points": 100,
  "path_to_graph": "/path/to/graph.png",
  "download_url": "/download/bubble_sort_20240204_123456.png",
  "graph_base64": "data:image/png;base64,iVBORw0KG...",
  "database": {
    "saved": true,
    "id": 1,
    "status_code": 201,
    "message": "Algorithm analysis saved successfully with ID: 1"
  }
}
```

### 3. Get All History - GET `/history`

Retrieves all saved analysis records from the database.

**Example:**
```bash
GET http://localhost:3000/history
```

**Response:**
```json
{
  "status": "success",
  "status_code": 200,
  "count": 5,
  "data": [
    {
      "id": 1,
      "algo": "Bubble Sort",
      "items": 1000,
      "steps": 10,
      "total_time_ms": 3,
      "time_complexity": "O(n²)",
      "created_at": "2024-02-04T12:34:56.789"
    }
  ]
}
```

### 4. Get Specific Record - GET `/history/<id>`

Retrieves a specific analysis record by ID.

**Example:**
```bash
GET http://localhost:3000/history/1
```

**Response:**
```json
{
  "status": "success",
  "status_code": 200,
  "data": {
    "id": 1,
    "algo": "Bubble Sort",
    "items": 1000,
    "steps": 10,
    "start_time": 36458241,
    "end_time": 239759234,
    "total_time_ms": 3,
    "time_complexity": "O(n²)",
    "path_to_graph": "/graphs/bubble_sort.png",
    "created_at": "2024-02-04T12:34:56.789"
  }
}
```

### 5. List Algorithms - GET `/algorithms`

Lists all available algorithms with their complexity notations.

**Response:**
```json
{
  "algorithms": [
    {"key": "bubble", "name": "Bubble Sort", "complexity": "O(n²)"},
    {"key": "linear", "name": "Linear Search", "complexity": "O(n)"},
    {"key": "binary", "name": "Binary Search", "complexity": "O(log n)"},
    {"key": "nested", "name": "Nested Loops", "complexity": "O(n²)"}
  ]
}
```

### 6. List Saved Graphs - GET `/graphs`

Lists all saved graph images.

**Response:**
```json
{
  "graphs": [
    {
      "filename": "bubble_sort_20240204_123456.png",
      "download_url": "/download/bubble_sort_20240204_123456.png"
    }
  ],
  "total": 1
}
```

### 7. Download Graph - GET `/download/<filename>`

Downloads a specific saved graph image.

**Example:**
```bash
GET http://localhost:3000/download/bubble_sort_20240204_123456.png
```

---

## Usage Examples

### Example 1: Run Flask App with Auto-Save
```bash
python app.py
```
Visit: `http://localhost:3000/analyze?algo=bubble&n=1000&steps=10`

### Example 2: Test Database Directly
```bash
python test_database.py
```
This will test connection, create tables, save data, and retrieve records.

### Example 3: Initialize Database Tables
```bash
python sqlachemy.py.py
```

### Example 4: Using Python Code
```python
from sqlachemy import save_analysis_result, get_analysis_by_id

# Save analysis result
data = {
    "algo": "Bubble Sort",
    "items": 1000,
    "steps": 10,
    "start_time": 36458241,
    "end_time": 239759234,
    "total_time_ms": 3,
    "time_complexity": "O(n²)",
    "path_to_graph": "/graphs/bubble_sort.png"
}

result = save_analysis_result(data)
print(f"Saved with ID: {result['id']}")

# Retrieve saved record
record = get_analysis_by_id(result['id'])
print(record['data'])
```

### Example 5: cURL Requests
```bash
# Analyze bubble sort
curl "http://localhost:3000/analyze?algo=bubble&n=1000&steps=10"

# Get all history
curl "http://localhost:3000/history"

# Get specific record
curl "http://localhost:3000/history/1"

# List algorithms
curl "http://localhost:3000/algorithms"
```

---

## Testing

### Test Database Functionality
```bash
python test_database.py
```

**Expected Output:**
```
======================================================================
Testing Algorithm Analysis Database
======================================================================

[STEP 1] Testing database connection...
✅ Connection successful!

[STEP 2] Initializing database tables...
✅ Tables created successfully!

[STEP 3] Saving algorithm analysis result...
✅ Data saved successfully!
   Status Code: 201
   Record ID: 1
   Message: Algorithm analysis saved successfully with ID: 1

[STEP 4] Retrieving saved record (ID: 1)...
✅ Record retrieved successfully!

[STEP 5] Retrieving all records...
✅ Retrieved 1 record(s)

======================================================================
Testing complete!
======================================================================
```

### Test Flask Endpoints
```bash
# Start the server
python app.py

# In another terminal, test endpoints
curl http://localhost:3000/
curl "http://localhost:3000/analyze?algo=bubble&n=100&steps=10"
curl http://localhost:3000/history
curl http://localhost:3000/algorithms
```

---

## Project Structure

```
HOME_ACTIVITY/complexity_visualizer_temp/
│
├── app.py                    # Main Flask application with database integration
├── sqlachemy.py.py          # Database module (models & functions)
├── factorial.py             # Factorial algorithm example
├── test_database.py         # Database testing script
│
├── requirements.txt         # Python dependencies
├── create_database.sql      # SQL setup script
│
├── README.md               # This comprehensive guide
├── DATABASE_GUIDE.md       # Detailed database documentation
├── QUICKSTART.md          # Quick reference guide
├── TASK_COMPLETION.md     # Task completion report
│
├── graphs/                 # Saved graph images
│   └── *.png
│
└── .venv/                  # Virtual environment (created by you)
```

### Key Files

| File | Purpose |
|------|---------|
| `app.py` | Flask API with algorithm analysis & database integration |
| `sqlachemy.py.py` | SQLAlchemy models, database functions, table definitions |
| `test_database.py` | Complete test suite for database operations |
| `requirements.txt` | All Python dependencies (Flask, SQLAlchemy, PyMySQL, etc.) |
| `create_database.sql` | SQL script to manually create database & tables |

---

## Available Algorithms

| Algorithm | Key | Time Complexity | Description |
|-----------|-----|-----------------|-------------|
| **Bubble Sort** | `bubble` | O(n²) | Classic sorting algorithm with nested loops |
| **Linear Search** | `linear` | O(n) | Sequential search through array |
| **Binary Search** | `binary` | O(log n) | Efficient search on sorted array |
| **Nested Loops** | `nested` | O(n²) | Demonstration of quadratic complexity |

---

## Database Functions

### Core Functions in `sqlachemy.py.py`

```python
# Initialize database and create tables
init_database()

# Save analysis result (returns status code & ID)
save_analysis_result(data)

# Retrieve specific record by ID
get_analysis_by_id(analysis_id)

# Retrieve all records
get_all_analyses()

# Test database connection
test_connection()
```

### Success Response Format
```json
{
  "status": "success",
  "status_code": 201,
  "id": 1,
  "message": "Algorithm analysis saved successfully with ID: 1",
  "data": {
    "id": 1,
    "algo": "Bubble Sort",
    "items": 1000,
    "steps": 10,
    "start_time": 36458241,
    "end_time": 239759234,
    "total_time_ms": 3,
    "time_complexity": "O(n²)",
    "path_to_graph": "/graphs/bubble_sort.png",
    "created_at": "2024-02-04T12:34:56.789"
  }
}
```

---

## Troubleshooting

### Database Connection Failed
**Problem:** `Connection failed: Can't connect to MySQL server`

**Solution:**
- Ensure MySQL/XAMPP is running
- Verify database credentials in `sqlachemy.py.py`
- Check if database exists: `CREATE DATABASE alchemy;`
- Test connection: `python sqlachemy.py.py`

### Import Error: No module named 'pymysql'
**Problem:** Missing PyMySQL dependency

**Solution:**
```bash
pip install pymysql
```

### Import Error: No module named 'sqlalchemy'
**Problem:** Missing SQLAlchemy dependency

**Solution:**
```bash
pip install sqlalchemy
```

### Table Already Exists
**Problem:** `Table 'algorithm_analysis' already exists`

**Solution:**
- This is normal! Tables are created automatically
- Safe to ignore - tables won't be duplicated

### Database Not Enabled
**Problem:** `{"error": "Database not enabled"}`

**Solution:**
- Ensure `sqlachemy.py.py` is in the same directory as `app.py`
- Check for import errors in terminal output
- Install missing dependencies: `pip install -r requirements.txt`

### Port Already in Use
**Problem:** `Address already in use`

**Solution:**
```bash
# Kill process on port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:3000 | xargs kill -9
```

---

## Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| `200` | Success | GET requests (retrieve data) |
| `201` | Created | POST/save operations |
| `400` | Bad Request | Invalid parameters |
| `404` | Not Found | Record/resource doesn't exist |
| `500` | Server Error | Database or server issues |
| `503` | Service Unavailable | Database disabled |

---

## Dependencies

```txt
Flask==3.0.0          # Web framework
numpy==1.24.3         # Numerical operations
matplotlib==3.7.2     # Graph generation
SQLAlchemy==2.0.23    # Database ORM
PyMySQL==1.1.0        # MySQL connector
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## Task Completion Summary

This project successfully implements:

1. **Database Table**: Created `algorithm_analysis` table with proper schema
2. **Data Persistence**: Automatically saves all analysis results to database
3. **Success Response**: Returns status code 201 with saved instance ID
4. **History Tracking**: API endpoints to retrieve past analyses
5. **Complete Integration**: Flask app fully integrated with SQLAlchemy
6. **Comprehensive Testing**: Test scripts for all functionality
7. **Full Documentation**: Multiple guide documents for easy reference

---

## Running the Application

### Start the Server
```bash
python app.py
```

**Output:**
```
==================================================
Algorithm Complexity Visualizer API
==================================================
Initializing database...
✓ Database tables created successfully!
Database ready!
Server running at: http://localhost:3000
Example: http://localhost:3000/analyze?algo=bubble&n=1000&steps=10
==================================================
 * Running on http://0.0.0.0:3000
```

### Make Your First Request
```bash
curl "http://localhost:3000/analyze?algo=bubble&n=1000&steps=10"
```

The response will include:
- Algorithm analysis results
- Generated graph (base64 encoded)
- Database save confirmation with ID
- Download URL for graph image
 
 
