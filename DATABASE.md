# Conversa Database Documentation

## Overview

The Conversa database uses **PostgreSQL 15** with an optimized schema for storing people, conversations, and action items.

## Database Information

- **Database Name**: `conversa`
- **PostgreSQL Version**: 15.15
- **Location**: `/opt/homebrew/var/postgresql@15`
- **Connection**: `postgresql://localhost/conversa`

## Schema Overview

### Tables

1. **people** - Stores information about individuals
2. **conversations** - Stores conversation/meeting records
3. **action_items** - Stores tasks associated with conversations

### Views

1. **people_summary** - People with conversation counts and pending actions
2. **recent_conversations** - Recent conversations with action item counts

---

## Table Structures

### 1. people

Stores information about individuals you interact with.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(20) | PRIMARY KEY | Unique identifier (e.g., "p1", "p2abc123") |
| name | VARCHAR(255) | NOT NULL | Person's full name |
| role | VARCHAR(255) | NOT NULL | Job title or role |
| avatar_color | VARCHAR(50) | NOT NULL, DEFAULT 'bg-indigo-200' | Tailwind CSS color class |
| context | TEXT | NOT NULL | How you know this person |
| interests | TEXT[] | DEFAULT '{}' | Array of interests/hobbies |
| open_follow_ups | TEXT[] | DEFAULT '{}' | Array of pending tasks |
| last_met | VARCHAR(50) | NULLABLE | Last meeting date (e.g., "Jan 16") |
| met_count | INTEGER | DEFAULT 0 | Number of times met |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Last update time |

**Indexes:**
- `people_pkey` - PRIMARY KEY on id
- `idx_people_name` - B-tree index on name
- `idx_people_last_met` - B-tree index on last_met
- `idx_people_met_count` - B-tree index on met_count (DESC)

**Constraints:**
- `people_name_check` - name must have length > 0
- `people_role_check` - role must have length > 0
- `people_met_count_check` - met_count >= 0

**Triggers:**
- `update_people_updated_at` - Auto-updates updated_at on record modification

**Example Data:**
```sql
INSERT INTO people (id, name, role, avatar_color, context, interests, open_follow_ups)
VALUES (
    'p1',
    'Sarah Chen',
    'Product Lead at Orio',
    'bg-indigo-200',
    'Met at the Design Systems conference last year.',
    ARRAY['Ethical AI', 'Hiking', 'Ceramics'],
    ARRAY['Send the Q3 proposal deck']
);
```

---

### 2. conversations

Stores conversation and meeting records.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(20) | PRIMARY KEY | Unique identifier (e.g., "c1", "c2abc123") |
| person_id | VARCHAR(20) | NOT NULL, FOREIGN KEY → people(id) ON DELETE CASCADE | Primary person in conversation |
| participants | TEXT[] | DEFAULT '{}' | Array of participant IDs |
| title | VARCHAR(500) | NOT NULL | Conversation title/topic |
| date | VARCHAR(50) | NOT NULL | Formatted date (e.g., "Jan 16 • 2:30 PM") |
| location | VARCHAR(255) | NOT NULL | Where conversation took place |
| summary | TEXT | NOT NULL | Brief summary of conversation |
| key_points | TEXT[] | DEFAULT '{}' | Important takeaways |
| full_transcript | TEXT | NULLABLE | Complete conversation transcript |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Last update time |

**Indexes:**
- `conversations_pkey` - PRIMARY KEY on id
- `idx_conversations_person_id` - B-tree index on person_id
- `idx_conversations_date` - B-tree index on date
- `idx_conversations_title` - B-tree index on title
- `idx_conversations_created_at` - B-tree index on created_at (DESC)
- `idx_conversations_search` - GIN index for full-text search

**Constraints:**
- `conversations_title_check` - title must have length > 0
- `conversations_location_check` - location must have length > 0

**Foreign Keys:**
- `conversations_person_id_fkey` - References people(id) ON DELETE CASCADE

**Triggers:**
- `update_conversations_updated_at` - Auto-updates updated_at on record modification

**Example Data:**
```sql
INSERT INTO conversations (id, person_id, participants, title, date, location, summary, key_points)
VALUES (
    'c1',
    'p1',
    ARRAY['p1', 'p3'],
    'Q3 Beta Roadmap Review',
    'Jan 16 • 2:30 PM',
    'Blue Bottle Coffee',
    'Discussed the roadmap for the Q3 beta launch.',
    ARRAY['Sarah thinks the sign-up process has too many steps.', 'She is available next Tuesday for a design review.']
);
```

---

### 3. action_items

Stores tasks and follow-up items from conversations.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(20) | PRIMARY KEY | Unique identifier (e.g., "a1", "a2abc123") |
| conversation_id | VARCHAR(20) | NOT NULL, FOREIGN KEY → conversations(id) ON DELETE CASCADE | Associated conversation |
| text | VARCHAR(500) | NOT NULL | Task description |
| completed | BOOLEAN | DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Last update time |

**Indexes:**
- `action_items_pkey` - PRIMARY KEY on id
- `idx_action_items_conversation_id` - B-tree index on conversation_id
- `idx_action_items_completed` - B-tree index on completed

**Constraints:**
- `action_items_text_check` - text must have length > 0

**Foreign Keys:**
- `action_items_conversation_id_fkey` - References conversations(id) ON DELETE CASCADE

**Triggers:**
- `update_action_items_updated_at` - Auto-updates updated_at on record modification

**Example Data:**
```sql
INSERT INTO action_items (id, conversation_id, text, completed)
VALUES ('a1', 'c1', 'Mock up a shortened onboarding flow', false);
```

---

## Views

### 1. people_summary

Aggregated view of people with their conversation and action item statistics.

**Columns:**
- All columns from `people` table
- `total_conversations` - Count of associated conversations
- `pending_actions` - Count of incomplete action items

**Usage:**
```sql
SELECT * FROM people_summary WHERE pending_actions > 0;
```

---

### 2. recent_conversations

Recent conversations with action item statistics.

**Columns:**
- All columns from `conversations` table
- `person_name` - Name of primary person
- `total_action_items` - Total count of action items
- `pending_action_items` - Count of incomplete action items

**Usage:**
```sql
SELECT * FROM recent_conversations LIMIT 10;
```

---

## Relationships

```
people (1) ----< (Many) conversations
                    |
                    |
                    v
                (Many) action_items
```

- One person can have many conversations
- One conversation belongs to one primary person
- One conversation can have many action items
- Cascade delete: Deleting a person deletes all their conversations
- Cascade delete: Deleting a conversation deletes all its action items

---

## Database Functions

### update_updated_at_column()

Automatically updates the `updated_at` timestamp when a record is modified.

**Definition:**
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';
```

**Applied to:**
- people table
- conversations table
- action_items table

---

## Common Queries

### Get all people with their conversation counts
```sql
SELECT * FROM people_summary ORDER BY total_conversations DESC;
```

### Search conversations by content
```sql
SELECT * FROM conversations
WHERE to_tsvector('english', title || ' ' || summary || ' ' || COALESCE(full_transcript, ''))
      @@ plainto_tsquery('english', 'design system');
```

### Get pending action items for a person
```sql
SELECT p.name, c.title, ai.text
FROM people p
JOIN conversations c ON p.id = c.person_id
JOIN action_items ai ON c.id = ai.conversation_id
WHERE ai.completed = false
  AND p.id = 'p1';
```

### Get recent conversations with action item counts
```sql
SELECT * FROM recent_conversations LIMIT 10;
```

### Get people sorted by last interaction
```sql
SELECT * FROM people
WHERE last_met IS NOT NULL
ORDER BY last_met DESC;
```

### Count conversations by person
```sql
SELECT p.name, COUNT(c.id) as conversation_count
FROM people p
LEFT JOIN conversations c ON p.id = c.person_id
GROUP BY p.id, p.name
ORDER BY conversation_count DESC;
```

---

## Database Management

### Backup Database
```bash
pg_dump conversa > backup_$(date +%Y%m%d).sql
```

### Restore Database
```bash
psql conversa < backup_20260118.sql
```

### Reset Database
```bash
# Drop and recreate
dropdb conversa
createdb conversa
psql -d conversa -f init_database.sql
```

### Check Database Size
```sql
SELECT pg_size_pretty(pg_database_size('conversa'));
```

### List All Tables
```bash
psql -d conversa -c "\dt"
```

### View Table Structure
```bash
psql -d conversa -c "\d people"
```

---

## Performance Optimization

### Indexes

All performance-critical fields have indexes:
- **people.name** - For name searches
- **people.last_met** - For sorting by recent interaction
- **conversations.person_id** - For filtering by person
- **conversations.date** - For date-based queries
- **conversations (full-text)** - For searching conversations
- **action_items.completed** - For filtering pending tasks

### Query Performance Tips

1. **Use indexes** - All common queries are indexed
2. **Use views** - Pre-computed aggregations available
3. **Limit results** - Use LIMIT for large datasets
4. **Use prepared statements** - FastAPI/SQLAlchemy handles this automatically

---

## Security Considerations

### Current Setup (Development)
- No authentication required
- Database owned by local user
- Suitable for local development only

### Production Recommendations
1. Create dedicated database user
2. Use strong password
3. Enable SSL connections
4. Restrict network access
5. Enable row-level security if multi-tenant
6. Regular backups
7. Use environment variables for credentials

### Create Production User
```sql
CREATE USER conversa_user WITH PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE conversa TO conversa_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO conversa_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO conversa_user;
```

---

## Maintenance Tasks

### Vacuum Database (Clean up)
```sql
VACUUM ANALYZE;
```

### Reindex Database
```sql
REINDEX DATABASE conversa;
```

### Check Index Usage
```sql
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### Find Unused Indexes
```sql
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE '%_pkey';
```

---

## Troubleshooting

### Connection Issues
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Start PostgreSQL
brew services start postgresql@15

# Check connection
psql -d conversa -c "SELECT version();"
```

### Permission Issues
```sql
-- Grant permissions to current user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO kevin;
```

### Database Doesn't Exist
```bash
# Recreate database
./setup_database.sh
```

---

## File Locations

- **Database data**: `/opt/homebrew/var/postgresql@15/`
- **Configuration**: `/opt/homebrew/etc/postgresql@15/`
- **Init script**: `init_database.sql`
- **Setup script**: `setup_database.sh`
- **Seed data**: `seed_data.py`

---

## Next Steps

1. ✅ Database created and initialized
2. ⏭️ Seed with sample data: `python seed_data.py`
3. ⏭️ Start the API server: `./run.sh`
4. ⏭️ Test API endpoints: http://localhost:8000/docs
