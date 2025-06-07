# Django Messaging API

## Overview

This project is a RESTful API for a messaging system built using Django and Django REST Framework (DRF). It allows users to start conversations, send messages, and retrieve their chat history.

## Features
- User authentication and profile management.
- Create and manage conversations with multiple participants.
- Send and retrieve messages in real-time.
- RESTful API endpoints for seamless integration.

## Technologies Used
- **Django** - Web framework for building scalable applications.
- **Django REST Framework (DRF)** - Simplifies API development.
- **PostgreSQL (or SQLite)** - Database for storing users, conversations, and messages.
- **Pillow** - Required for handling images in user profiles.


## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/alx-backend-python/messaging_app.git
cd messaging_app
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the server
```bash
python manage.py runserver
```

# API Endpints

## API Overview
This API provides endpoints for user management, conversations, and messages. It follows RESTful conventions and is built using Django REST Framework.

## Base URL
http://127.0.0.1:8000/api/


## User Management Endpoints
| Method | Endpoint | Description |
|--------|---------|------------|
| `POST` | `/users/register/` | Register a new user |
| `GET`  | `/users/{id}/` | Retrieve user details |

## Conversation Endpoints
| Method | Endpoint | Description |
|--------|---------|------------|
| `GET`  | `/conversations/` | List all conversations |
| `POST` | `/conversations/` | Create a new conversation |
| `GET`  | `/conversations/{id}/` | Retrieve details of a specific conversation |

## Message Endpoints
| Method | Endpoint | Description |
|--------|---------|------------|
| `GET`  | `/messages/` | Retrieve all messages |
| `POST` | `/messages/` | Send a new message |
| `GET`  | `/messages/{id}/` | Retrieve details of a specific message |

## Authentication
- Ensure authentication is set up for secure access.
- Use token-based authentication or JWT authentication for authorization.

## Response Format
All API responses are in JSON format.

