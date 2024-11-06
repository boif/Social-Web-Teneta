# Django Project

This project is a Django application with real-time chat, news posts, and user profiles. It uses Django Channels for WebSocket support and PostgreSQL as the database. Redis is used for caching and real-time features.

## Features

- **Real-time chat**: Supports private and group chats.
- **Posts and comments**: Users can create, like, and comment on posts.
- **User profiles**: Each user has a profile with an optional picture and description.
- **Django Channels**: For handling WebSocket connections.
  
## Requirements

- Python 3.10 or higher
- PostgreSQL 13 or higher
- Redis (for caching and WebSocket management)

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/boif/Social-Web-Teneta.git
cd Teneta
```

### Step 2: Build Docker containers

## Make sure Docker and Docker Compose are installed, then build the containers:
```
docker-compose build
```
### Step 3: Run the project

## After building the containers, run the following command to start the project:
```
docker-compose up
```
This will start the following services:

    Web: The Django application running on port 8000.
    Database: PostgreSQL running on port 5434.
    Redis: Redis service running on port 6379.

The application will be available at http://localhost:8000.
