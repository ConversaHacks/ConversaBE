-- Conversa Database Schema
-- PostgreSQL 15+

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS action_items CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS people CASCADE;

-- Drop existing functions
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Create update timestamp function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- =====================================================
-- Table: people
-- =====================================================
CREATE TABLE people (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    avatar_color VARCHAR(50) NOT NULL DEFAULT 'bg-indigo-200',
    context TEXT NOT NULL,
    interests TEXT[] DEFAULT '{}',
    open_follow_ups TEXT[] DEFAULT '{}',
    last_met VARCHAR(50),
    met_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT people_name_check CHECK (length(name) > 0),
    CONSTRAINT people_role_check CHECK (length(role) > 0),
    CONSTRAINT people_met_count_check CHECK (met_count >= 0)
);

-- Create indexes for people table
CREATE INDEX idx_people_name ON people(name);
CREATE INDEX idx_people_last_met ON people(last_met);
CREATE INDEX idx_people_met_count ON people(met_count DESC);

-- Create trigger for people updated_at
CREATE TRIGGER update_people_updated_at
    BEFORE UPDATE ON people
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- Table: conversations
-- =====================================================
CREATE TABLE conversations (
    id VARCHAR(20) PRIMARY KEY,
    person_id VARCHAR(20) NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    participants TEXT[] DEFAULT '{}',
    title VARCHAR(500) NOT NULL,
    date VARCHAR(50) NOT NULL,
    location VARCHAR(255) NOT NULL,
    summary TEXT NOT NULL,
    key_points TEXT[] DEFAULT '{}',
    full_transcript TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT conversations_title_check CHECK (length(title) > 0),
    CONSTRAINT conversations_location_check CHECK (length(location) > 0)
);

-- Create indexes for conversations table
CREATE INDEX idx_conversations_person_id ON conversations(person_id);
CREATE INDEX idx_conversations_date ON conversations(date);
CREATE INDEX idx_conversations_title ON conversations(title);
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);

-- Create full-text search index for searching conversations
CREATE INDEX idx_conversations_search ON conversations
USING gin(to_tsvector('english', title || ' ' || summary || ' ' || COALESCE(full_transcript, '')));

-- Create trigger for conversations updated_at
CREATE TRIGGER update_conversations_updated_at
    BEFORE UPDATE ON conversations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- Table: action_items
-- =====================================================
CREATE TABLE action_items (
    id VARCHAR(20) PRIMARY KEY,
    conversation_id VARCHAR(20) NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    text VARCHAR(500) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT action_items_text_check CHECK (length(text) > 0)
);

-- Create indexes for action_items table
CREATE INDEX idx_action_items_conversation_id ON action_items(conversation_id);
CREATE INDEX idx_action_items_completed ON action_items(completed);

-- Create trigger for action_items updated_at
CREATE TRIGGER update_action_items_updated_at
    BEFORE UPDATE ON action_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- Helpful Views (Optional)
-- =====================================================

-- View: People with their conversation count
CREATE OR REPLACE VIEW people_summary AS
SELECT
    p.*,
    COUNT(c.id) as total_conversations,
    COUNT(CASE WHEN ai.completed = false THEN 1 END) as pending_actions
FROM people p
LEFT JOIN conversations c ON p.id = c.person_id
LEFT JOIN action_items ai ON c.id = ai.conversation_id
GROUP BY p.id;

-- View: Recent conversations
CREATE OR REPLACE VIEW recent_conversations AS
SELECT
    c.*,
    p.name as person_name,
    COUNT(ai.id) as total_action_items,
    COUNT(CASE WHEN ai.completed = false THEN 1 END) as pending_action_items
FROM conversations c
JOIN people p ON c.person_id = p.id
LEFT JOIN action_items ai ON c.id = ai.conversation_id
GROUP BY c.id, p.name
ORDER BY c.created_at DESC;

-- =====================================================
-- Grant Permissions (if using specific user)
-- =====================================================
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO conversa_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO conversa_user;

-- =====================================================
-- Success Message
-- =====================================================
DO $$
BEGIN
    RAISE NOTICE 'Database schema created successfully!';
    RAISE NOTICE 'Tables created: people, conversations, action_items';
    RAISE NOTICE 'Indexes created for optimal performance';
    RAISE NOTICE 'Triggers added for automatic timestamp updates';
    RAISE NOTICE 'Views created: people_summary, recent_conversations';
END $$;
