# ConversaBE - Project Structure

## Directory Tree

```
ConversaBE/
├── app/
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # FastAPI application entry point
│   │
│   ├── core/                       # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py              # App settings and environment variables
│   │   └── database.py            # Database connection and session management
│   │
│   ├── models/                     # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── person.py              # Person database model
│   │   └── conversation.py        # Conversation & ActionItem models
│   │
│   ├── schemas/                    # Pydantic schemas for validation
│   │   ├── __init__.py
│   │   ├── person.py              # Person request/response schemas
│   │   └── conversation.py        # Conversation & ActionItem schemas
│   │
│   └── routers/                    # API route handlers
│       ├── __init__.py
│       ├── people.py              # People CRUD endpoints
│       └── conversations.py       # Conversations CRUD endpoints
│
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── run.sh                          # Quick start script
├── seed_data.py                    # Database seeding script
├── README.md                       # Main documentation
├── API_SCHEMA.md                   # Detailed API schema documentation
└── PROJECT_STRUCTURE.md            # This file
```

## File Purposes

### Core Files

#### `app/main.py`
- FastAPI application initialization
- CORS middleware configuration
- Router registration
- Health check endpoints
- API documentation setup

#### `app/core/config.py`
- Application settings using Pydantic BaseSettings
- Environment variable management
- Database URL configuration
- CORS origins setup

#### `app/core/database.py`
- SQLAlchemy engine creation
- Database session factory
- Base model class
- Database dependency injection

### Models Layer (`app/models/`)

#### `person.py`
**Person Model**
- Represents individuals in the system
- Fields: id, name, role, avatar_color, context, interests, open_follow_ups, last_met, met_count
- Relationship: One-to-Many with Conversations

#### `conversation.py`
**Conversation Model**
- Represents conversations/meetings
- Fields: id, person_id, participants, title, date, location, summary, key_points, full_transcript
- Relationship: Many-to-One with Person, One-to-Many with ActionItems

**ActionItem Model**
- Represents tasks from conversations
- Fields: id, conversation_id, text, completed
- Relationship: Many-to-One with Conversation

### Schemas Layer (`app/schemas/`)

Defines request/response data structures using Pydantic:

#### `person.py`
- `PersonBase` - Base fields
- `PersonCreate` - For creating new people
- `PersonUpdate` - For updating existing people (all fields optional)
- `PersonResponse` - Full person data with timestamps
- `PersonListResponse` - Simplified list view

#### `conversation.py`
- `ActionItemBase`, `ActionItemCreate`, `ActionItemUpdate`, `ActionItemResponse`
- `ConversationBase` - Base conversation fields
- `ConversationCreate` - For creating conversations with action items
- `ConversationUpdate` - For updating conversations (all fields optional)
- `ConversationResponse` - Full conversation data with action items
- `ConversationListResponse` - Simplified list view with action item count

### Routers Layer (`app/routers/`)

#### `people.py`
RESTful endpoints for people management:
- `GET /api/v1/people` - List all people
- `GET /api/v1/people/{person_id}` - Get single person
- `POST /api/v1/people` - Create person
- `PUT /api/v1/people/{person_id}` - Update person
- `DELETE /api/v1/people/{person_id}` - Delete person

#### `conversations.py`
RESTful endpoints for conversations:
- `GET /api/v1/conversations` - List all conversations (filterable by person_id)
- `GET /api/v1/conversations/{conversation_id}` - Get single conversation
- `POST /api/v1/conversations` - Create conversation with action items
- `PUT /api/v1/conversations/{conversation_id}` - Update conversation
- `DELETE /api/v1/conversations/{conversation_id}` - Delete conversation
- `PATCH /api/v1/conversations/{conversation_id}/action-items/{item_id}` - Toggle action item

### Utility Files

#### `seed_data.py`
- Populates database with sample data
- Matches the frontend mock data exactly
- Run after initial setup: `python seed_data.py`

#### `run.sh`
- Quick start script for development server
- Runs uvicorn with hot reload
- Usage: `./run.sh`

#### `requirements.txt`
Dependencies:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `psycopg2-binary` - PostgreSQL driver
- `pydantic` - Data validation
- `pydantic-settings` - Settings management
- `python-dotenv` - Environment variable loading

## Data Flow

### Creating a Conversation
```
Frontend Request
    ↓
POST /api/v1/conversations (conversations.py router)
    ↓
Validate with ConversationCreate schema (schemas/conversation.py)
    ↓
Check person exists in database
    ↓
Create Conversation model (models/conversation.py)
    ↓
Create ActionItem models
    ↓
Update Person met_count and last_met
    ↓
Commit to database
    ↓
Return ConversationResponse schema
    ↓
Frontend receives data
```

### Getting People List
```
Frontend Request
    ↓
GET /api/v1/people (people.py router)
    ↓
Query Person models from database
    ↓
Convert to PersonListResponse schemas
    ↓
Return JSON array
    ↓
Frontend receives data
```

## Database Schema

### Tables

**people**
```sql
CREATE TABLE people (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    avatar_color VARCHAR NOT NULL,
    context TEXT NOT NULL,
    interests TEXT[],
    open_follow_ups TEXT[],
    last_met VARCHAR,
    met_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**conversations**
```sql
CREATE TABLE conversations (
    id VARCHAR PRIMARY KEY,
    person_id VARCHAR REFERENCES people(id),
    participants TEXT[],
    title VARCHAR NOT NULL,
    date VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
    summary TEXT NOT NULL,
    key_points TEXT[],
    full_transcript TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**action_items**
```sql
CREATE TABLE action_items (
    id VARCHAR PRIMARY KEY,
    conversation_id VARCHAR REFERENCES conversations(id) ON DELETE CASCADE,
    text VARCHAR NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## API Architecture

### Layer Separation
1. **Routes** - Handle HTTP requests/responses, call business logic
2. **Schemas** - Validate input/output data
3. **Models** - Define database structure
4. **Core** - Provide configuration and database connections

### Design Patterns
- **Dependency Injection** - Database sessions via `Depends(get_db)`
- **Repository Pattern** - Direct SQLAlchemy queries in routes (can be extracted later)
- **DTO Pattern** - Pydantic schemas separate from ORM models
- **RESTful API** - Standard HTTP methods and status codes

### Error Handling
- `404 Not Found` - Resource doesn't exist
- `422 Unprocessable Entity` - Validation errors (automatic via Pydantic)
- `500 Internal Server Error` - Database or server errors

## Development Workflow

1. **Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with database credentials
   ```

2. **Initialize Database**
   ```bash
   python seed_data.py
   ```

3. **Run Server**
   ```bash
   ./run.sh
   # Or: uvicorn app.main:app --reload
   ```

4. **Test API**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Frontend Integration Points

The backend is designed to match the frontend's data structure exactly:

- **Field names** use snake_case in database, but can be configured to return camelCase
- **ID formats** match frontend expectations (p1, c1, a1)
- **Date formats** match frontend display (e.g., "Jan 16 • 2:30 PM")
- **Color classes** use Tailwind CSS format (e.g., "bg-indigo-200")

See [API_SCHEMA.md](API_SCHEMA.md) for detailed integration documentation.
