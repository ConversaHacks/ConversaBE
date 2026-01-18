# Conversa Backend API

A FastAPI-based backend service for the Conversa application - a conversation and relationship management system.

## Features

- **People Management**: Create, read, update, and delete person records with interests, context, and follow-ups
- **Conversation Management**: Track conversations with summaries, key points, transcripts, and action items
- **Action Items**: Manage tasks and follow-ups associated with conversations
- **RESTful API**: Clean, well-documented API endpoints
- **PostgreSQL Database**: Robust relational database for data persistence
- **Automatic Documentation**: Swagger UI and ReDoc available out of the box

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Database
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server

## Project Structure

```
ConversaBE/
├── app/
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   └── database.py        # Database connection and session
│   ├── models/
│   │   ├── person.py          # Person SQLAlchemy model
│   │   └── conversation.py    # Conversation & ActionItem models
│   ├── schemas/
│   │   ├── person.py          # Person Pydantic schemas
│   │   └── conversation.py    # Conversation Pydantic schemas
│   ├── routers/
│   │   ├── people.py          # People endpoints
│   │   └── conversations.py   # Conversation endpoints
│   └── main.py                # FastAPI application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL 12+

### 1. Clone the repository

```bash
cd /Users/kevin/Documents/ConversaMonorepo/ConversaBE
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL database

```bash
# Create a new PostgreSQL database
createdb conversa

# Or using psql:
psql -U postgres
CREATE DATABASE conversa;
\q
```

### 5. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your database credentials
```

Example `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost:5432/conversa
DEBUG=True
API_V1_PREFIX=/api/v1
```

### 6. Run the application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### People

- `GET /api/v1/people` - Get all people
- `GET /api/v1/people/{person_id}` - Get a specific person
- `POST /api/v1/people` - Create a new person
- `PUT /api/v1/people/{person_id}` - Update a person
- `DELETE /api/v1/people/{person_id}` - Delete a person

### Conversations

- `GET /api/v1/conversations` - Get all conversations (optional: filter by person_id)
- `GET /api/v1/conversations/{conversation_id}` - Get a specific conversation
- `POST /api/v1/conversations` - Create a new conversation
- `PUT /api/v1/conversations/{conversation_id}` - Update a conversation
- `DELETE /api/v1/conversations/{conversation_id}` - Delete a conversation
- `PATCH /api/v1/conversations/{conversation_id}/action-items/{item_id}` - Toggle action item completion

## Database Schema

### People Table
- `id`: String (Primary Key, auto-generated)
- `name`: String
- `role`: String
- `avatar_color`: String (Tailwind CSS class)
- `context`: Text
- `interests`: Array[String]
- `open_follow_ups`: Array[String]
- `last_met`: String (optional)
- `met_count`: Integer
- `created_at`: DateTime
- `updated_at`: DateTime

### Conversations Table
- `id`: String (Primary Key, auto-generated)
- `person_id`: String (Foreign Key to People)
- `participants`: Array[String]
- `title`: String
- `date`: String
- `location`: String
- `summary`: Text
- `key_points`: Array[String]
- `full_transcript`: Text (optional)
- `created_at`: DateTime
- `updated_at`: DateTime

### Action Items Table
- `id`: String (Primary Key, auto-generated)
- `conversation_id`: String (Foreign Key to Conversations)
- `text`: String
- `completed`: Boolean
- `created_at`: DateTime
- `updated_at`: DateTime

## Example API Usage

### Create a Person

```bash
curl -X POST "http://localhost:8000/api/v1/people" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Chen",
    "role": "Product Lead at Orio",
    "avatar_color": "bg-indigo-200",
    "context": "Met at the Design Systems conference last year.",
    "interests": ["Ethical AI", "Hiking", "Ceramics"],
    "open_follow_ups": ["Send the Q3 proposal deck"]
  }'
```

### Create a Conversation

```bash
curl -X POST "http://localhost:8000/api/v1/conversations" \
  -H "Content-Type: application/json" \
  -d '{
    "person_id": "p1",
    "participants": ["p1"],
    "title": "Q3 Beta Roadmap Review",
    "date": "Jan 16 • 2:30 PM",
    "location": "Blue Bottle Coffee",
    "summary": "Discussed the roadmap for the Q3 beta launch.",
    "key_points": ["Sarah thinks the sign-up process has too many steps."],
    "action_items": [
      {"text": "Mock up a shortened onboarding flow", "completed": false}
    ]
  }'
```

## Development

### Running Tests

```bash
# Tests coming soon
pytest
```

### Database Migrations

The application currently uses SQLAlchemy's `create_all()` to create tables automatically. For production, consider using Alembic for migrations:

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## CORS Configuration

The API is configured to accept requests from:
- http://localhost:5173 (Vite default)
- http://localhost:3000 (Common React port)

Update `CORS_ORIGINS` in your `.env` file to add more origins.

## License

MIT
# ConversaBE
