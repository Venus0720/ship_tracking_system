Ship Tracking System - Installation Guide

<!-- Antonio Hernández de la Rosa [Client] & Roman Plaksin [Developer] (03/12/2025) -->

Welcome to the Ship Tracking System! This guide will walk you through setting up the project step by step, even if you have no prior coding experience. Follow the instructions carefully to install and run the system.

Prerequisites

    Before you begin, ensure your system meets the following requirements:

Operating System:

    Windows, macOS, or Linux

- Required Software:

    Git (for downloading the project)["https://git-scm.com/downloads"]
    Node.js (for running the frontend, includes npm)["https://nodejs.org/en"]
    Python 3.8+ (for the backend)["https://www.python.org/downloads/"]
    Docker (for running PostgreSQL, RabbitMQ, and Redis)["https://www.docker.com/"]
    ArcGIS Developer Account (for API access)["https://developers.arcgis.com/"]


Step 1: After clone the Repository
Navigate into the project folder:
    cd ship-tracking-system

Step 2: Setup PostgreSQL Database
    1. Install PostgreSQL if you haven’t already.
    2. Open pgAdmin or psql and run the following commands to create the database and table:
```bash
    CREATE DATABASE shipsdb;

    \c shipsdb; -- Connect to the database

    CREATE TABLE ship_tracks (
        id SERIAL PRIMARY KEY,
        ship_id VARCHAR(50),
        latitude FLOAT,
        longitude FLOAT,
        speed FLOAT,
        heading INT,
        timestamp TIMESTAMP
    );

    SELECT * FROM ship_tracks;
```

    3. Update the PostgreSQL connection details in your backend:
```bash
    import psycopg2
    conn = psycopg2.connect(
        dbname="shipsdb",
        user="your_postgres_user",
        password="your_postgres_password",
        host="localhost",
        port="5432"
    )
```

Step 3: Configure RabbitMQ
    Set up RabbitMQ with the following credentials:

    RABBITMQ_DEFAULT_USER=guest
    RABBITMQ_DEFAULT_PASS=guest

Step 4: Install Backend Dependencies
    1. Navigate to the backend folder:
```bash
cd backend
```
    2. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

Step 5: Install frontend Dependencies
    1. Navigate to the backend folder:
```bash
cd frontend
```
    2. Install the required Python dependencies:
```bash
npm install
```

Step 6: Start Services with Docker
    Run the following command to start PostgreSQL, RabbitMQ, and Redis using Docker:
```bash
docker-compose up -d
```

Step 7: Start the Backend Server
    1. Navigate to the backend folder:
```bash
cd backend/websocket
```
Start the WebSocket backend server:
```bash
uvicorn websocket_server:app --host 0.0.0.0 --port 8000
```

Step 8: Start the Producer
    1. Navigate to the producer folder:
```bash
cd producer
python producer.py
```

Step 9: Start the Consumer
    1. Navigate to the consumer folder:
```bash
cd consumer
python consumer.py
```

Step 10: Start the Frontend Application
    1. Navigate to the frontend folder:
```bash
cd ship-tracker
```
Start the React application:
```bash
npom start
```

Troubleshooting
    If the backend doesn’t start, ensure Python and all dependencies are installed correctly.
    If the frontend doesn’t load, verify that all packages are installed with npm install.
    If WebSocket connections fail, check if the backend is running properly.
    If Docker services fail, restart Docker and re-run docker-compose up -d.

Support

If you need any assistance, please contact us at "[senusgodness0@gmail.com]" or refer to the project documentation.

Enjoy using the Ship Tracking System! 🚢

Thank you very much Antonio Hernández de la Rosa.🤝 Roman . Best Regards.

![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-4.png)
![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-7.png)
![alt text](image-8.png)