# Conversa API Schema Documentation

This document describes the exact data types and formats expected by the frontend application.

## Data Models

### Person

**Database Fields:**
```python
{
    "id": str,                      # Auto-generated (format: "p{8-char-hex}")
    "name": str,                    # Person's full name
    "role": str,                    # Job title or role
    "avatar_color": str,            # Tailwind CSS class (e.g., "bg-indigo-200")
    "last_met": str | null,         # Date string (e.g., "Jan 16")
    "met_count": int,               # Number of times met (default: 0)
    "interests": list[str],         # List of interests/hobbies
    "context": str,                 # How you know this person
    "open_follow_ups": list[str],   # List of pending tasks
    "created_at": datetime,         # Auto-generated timestamp
    "updated_at": datetime          # Auto-updated timestamp
}
```

**Frontend Expects (PersonListResponse):**
```typescript
{
    id: string,
    name: string,
    role: string,
    avatarColor: string,
    lastMet: string | null,
    metCount: number,
    context: string
}
```

**Frontend Expects (PersonDetail - PersonResponse):**
```typescript
{
    id: string,
    name: string,
    role: string,
    avatarColor: string,
    lastMet: string | null,
    metCount: number,
    interests: string[],
    context: string,
    openFollowUps: string[],
    created_at: string,
    updated_at: string
}
```

---

### Conversation

**Database Fields:**
```python
{
    "id": str,                      # Auto-generated (format: "c{8-char-hex}")
    "person_id": str,               # Foreign key to Person
    "participants": list[str],      # List of participant IDs
    "title": str,                   # Conversation title
    "date": str,                    # Formatted date (e.g., "Jan 16 • 2:30 PM")
    "location": str,                # Where conversation took place
    "summary": str,                 # Brief summary
    "key_points": list[str],        # Important takeaways
    "full_transcript": str | null,  # Full conversation text
    "created_at": datetime,         # Auto-generated timestamp
    "updated_at": datetime          # Auto-updated timestamp
}
```

**Frontend Expects (ConversationListResponse):**
```typescript
{
    id: string,
    personId: string,
    participants: string[],
    title: string,
    date: string,
    location: string,
    summary: string,
    activeActionItemsCount: number  // Computed: count of uncompleted action items
}
```

**Frontend Expects (ConversationDetail - ConversationResponse):**
```typescript
{
    id: string,
    personId: string,
    participants: string[],
    title: string,
    date: string,
    location: string,
    summary: string,
    keyPoints: string[],
    actionItems: ActionItem[],
    fullTranscript: string | null,
    created_at: string,
    updated_at: string
}
```

---

### Action Item

**Database Fields:**
```python
{
    "id": str,                      # Auto-generated (format: "a{8-char-hex}")
    "conversation_id": str,         # Foreign key to Conversation
    "text": str,                    # Action item description
    "completed": bool,              # Completion status (default: false)
    "created_at": datetime,         # Auto-generated timestamp
    "updated_at": datetime          # Auto-updated timestamp
}
```

**Frontend Expects:**
```typescript
{
    id: string,
    text: string,
    completed: boolean
}
```

---

## API Endpoints

### People Endpoints

#### GET /api/v1/people
Get all people.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response:** `PersonListResponse[]`

---

#### GET /api/v1/people/{person_id}
Get a specific person by ID.

**Path Parameters:**
- `person_id` (string): The person's ID

**Response:** `PersonResponse`

---

#### POST /api/v1/people
Create a new person.

**Request Body:**
```json
{
    "name": "Sarah Chen",
    "role": "Product Lead at Orio",
    "avatar_color": "bg-indigo-200",
    "context": "Met at the Design Systems conference last year.",
    "interests": ["Ethical AI", "Hiking", "Ceramics"],
    "open_follow_ups": ["Send the Q3 proposal deck"]
}
```

**Response:** `PersonResponse` (201 Created)

---

#### PUT /api/v1/people/{person_id}
Update a person's information.

**Path Parameters:**
- `person_id` (string): The person's ID

**Request Body:** All fields optional
```json
{
    "name": "Sarah Chen",
    "role": "VP of Product at Orio",
    "context": "Met at the Design Systems conference last year. Now looking for a co-founder."
}
```

**Response:** `PersonResponse`

---

#### DELETE /api/v1/people/{person_id}
Delete a person.

**Path Parameters:**
- `person_id` (string): The person's ID

**Response:** 204 No Content

---

### Conversation Endpoints

#### GET /api/v1/conversations
Get all conversations.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)
- `person_id` (string, optional): Filter conversations by person ID

**Response:** `ConversationListResponse[]`

---

#### GET /api/v1/conversations/{conversation_id}
Get a specific conversation by ID.

**Path Parameters:**
- `conversation_id` (string): The conversation's ID

**Response:** `ConversationResponse`

---

#### POST /api/v1/conversations
Create a new conversation.

**Request Body:**
```json
{
    "person_id": "p1",
    "participants": ["p1", "p3"],
    "title": "Q3 Beta Roadmap Review",
    "date": "Jan 16 • 2:30 PM",
    "location": "Blue Bottle Coffee",
    "summary": "Discussed the roadmap for the Q3 beta launch.",
    "key_points": [
        "Sarah thinks the sign-up process has too many steps.",
        "Suggests moving the 'Personalization' screen to after account creation."
    ],
    "full_transcript": "Sarah: Thanks for meeting up...",
    "action_items": [
        {"text": "Mock up a shortened onboarding flow", "completed": false},
        {"text": "Send calendar invite for Tuesday Design Review", "completed": false}
    ]
}
```

**Response:** `ConversationResponse` (201 Created)

**Note:** This endpoint automatically:
- Increments the person's `met_count`
- Updates the person's `last_met` date

---

#### PUT /api/v1/conversations/{conversation_id}
Update a conversation.

**Path Parameters:**
- `conversation_id` (string): The conversation's ID

**Request Body:** All fields optional
```json
{
    "title": "Updated Title",
    "summary": "Updated summary text"
}
```

**Response:** `ConversationResponse`

---

#### DELETE /api/v1/conversations/{conversation_id}
Delete a conversation.

**Path Parameters:**
- `conversation_id` (string): The conversation's ID

**Response:** 204 No Content

---

#### PATCH /api/v1/conversations/{conversation_id}/action-items/{item_id}
Toggle or update an action item.

**Path Parameters:**
- `conversation_id` (string): The conversation's ID
- `item_id` (string): The action item's ID

**Request Body:**
```json
{
    "completed": true
}
```

Or update the text:
```json
{
    "text": "Updated action item text",
    "completed": false
}
```

**Response:** `ConversationResponse` (returns the full updated conversation)

---

## Field Name Mapping (Python ↔ TypeScript)

The API uses snake_case (Python convention) for field names, but the frontend expects camelCase (TypeScript convention).

**Mapping:**
```
Python (API)          → TypeScript (Frontend)
avatar_color          → avatarColor
last_met              → lastMet
met_count             → metCount
open_follow_ups       → openFollowUps
person_id             → personId
key_points            → keyPoints
full_transcript       → fullTranscript
action_items          → actionItems
created_at            → created_at (kept as is)
updated_at            → updated_at (kept as is)
```

**Note:** The Pydantic models are configured with `class Config: from_attributes = True` to handle automatic snake_case to camelCase conversion when serializing responses.

---

## Example Frontend Integration

### Fetching People

```typescript
const response = await fetch('http://localhost:8000/api/v1/people');
const people = await response.json();
// people is PersonListResponse[]
```

### Creating a Conversation

```typescript
const newConversation = {
    person_id: "p1",
    participants: ["p1"],
    title: "Coffee Chat",
    date: "Jan 18 • 3:00 PM",
    location: "Starbucks",
    summary: "Caught up on recent projects",
    key_points: ["Working on new feature", "Launching in Q2"],
    action_items: [
        { text: "Share the design mockups", completed: false }
    ]
};

const response = await fetch('http://localhost:8000/api/v1/conversations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newConversation)
});

const conversation = await response.json();
// conversation is ConversationResponse
```

### Toggling an Action Item

```typescript
const response = await fetch(
    `http://localhost:8000/api/v1/conversations/c1/action-items/a1`,
    {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: true })
    }
);

const updatedConversation = await response.json();
// updatedConversation is ConversationResponse with updated action item
```

---

## Database Setup

The backend uses PostgreSQL with the following table structure:

**Tables:**
1. `people` - Stores person records
2. `conversations` - Stores conversation records
3. `action_items` - Stores action items linked to conversations

**Relationships:**
- `conversations.person_id` → `people.id` (Many-to-One)
- `action_items.conversation_id` → `conversations.id` (Many-to-One, cascade delete)
- `conversations.participants` → Array of `people.id` (logical reference, not FK)

**Auto-generated IDs:**
- People: `p{8-char-hex}` (e.g., "p1", "p2abc123")
- Conversations: `c{8-char-hex}` (e.g., "c1", "c2def456")
- Action Items: `a{8-char-hex}` (e.g., "a1", "a3ghi789")
