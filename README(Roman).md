Real-Time Ship Tracking and Analytics System

Overview

The Real-Time Ship Tracking and Analytics System is a distributed microservices application designed to simulate, process, and visualize ship movements in real time. The system generates synthetic ship data, processes it through multiple consumer services, and displays live updates and insights on an interactive map using ReactJS and the ArcGIS Web SDK.

- Features

Real-time Ship Position Simulation: Producers generate synthetic ship track data.
Message Broker: RabbitMQ enables asynchronous communication between producers and consumers.
Parallel Processing: Consumers process ship data concurrently.
Insights Generation: Compute analytics such as congestion zones and speed anomalies.
Data Persistence: PostgreSQL for raw and processed data storage.
Caching Layer: Redis optimizes performance with frequently accessed data.
Live Map Visualization: ReactJS frontend with ArcGIS Web SDK displays real-time ship locations.
Scalability: Horizontally scalable microservices architecture.
Containerized Deployment: Docker Compose setup for seamless execution.

System Architecture

The system follows a microservices-based architecture with the following components:

1. Backend Microservices

Producers (Ship Data Generators)
Simulate real-time ship movement.
Publish messages to RabbitMQ with:
Ship ID
Latitude & Longitude
Heading/Position
Speed (optional)
Timestamp
Message Broker (RabbitMQ)
Handles message routing between producers and consumers.
Ensures parallel processing of ship data.
Consumers (Ship Data Processors)
Subscribe to RabbitMQ and process incoming ship data.
Perform tasks such as:
Data Aggregation: Compute average speeds, detect anomalies.
Clustering Analysis: Identify congested maritime regions.
Real-time Insights: Highlight abnormal speed changes and high-density zones.
Store raw and processed data in PostgreSQL.
Caching Layer (Redis)
Stores frequently accessed ship positions for fast retrieval.

2. Frontend Application

ReactJS & ArcGIS Web SDK
Interactive map visualization of real-time ship locations.
Displays ship tracks and overlays insights (e.g., heatmaps for congestion zones).
WebSocket Integration
Enables real-time updates to reflect:
New ship positions
Updated insights from consumer processing
66.42.95.64





```bash

\c shipsdb;
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
\d

PostgreSQL run
"C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe" start -D "C:\Program Files\PostgreSQL\17\data"

Option 2: Install Redis via Docker
If you have Docker installed, you can run Redis as a container:

docker run --name redis -p 6379:6379 -d redis

Then check if Redis is running:
docker ps

web socket running.
uvicorn websocket_server:app --host 0.0.0.0 --port 8000