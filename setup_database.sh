#!/bin/bash

# Conversa Database Setup Script
# This script creates and initializes the PostgreSQL database

set -e  # Exit on error

echo "======================================"
echo "Conversa Database Setup"
echo "======================================"
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed."
    echo "Installing PostgreSQL via Homebrew..."
    brew install postgresql@15
    brew services start postgresql@15
    echo "✓ PostgreSQL installed and started"
else
    echo "✓ PostgreSQL is already installed"
fi

# Database name
DB_NAME="conversa"

# Check if database exists
if /opt/homebrew/opt/postgresql@15/bin/psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo ""
    echo "⚠️  Database '$DB_NAME' already exists."
    read -p "Do you want to drop and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Dropping existing database..."
        /opt/homebrew/opt/postgresql@15/bin/dropdb $DB_NAME
        echo "Creating new database..."
        /opt/homebrew/opt/postgresql@15/bin/createdb $DB_NAME
        echo "✓ Database recreated"
    else
        echo "Skipping database creation"
    fi
else
    echo "Creating database '$DB_NAME'..."
    /opt/homebrew/opt/postgresql@15/bin/createdb $DB_NAME
    echo "✓ Database created"
fi

# Run schema initialization
echo ""
echo "Running schema initialization..."
/opt/homebrew/opt/postgresql@15/bin/psql -d $DB_NAME -f init_database.sql

echo ""
echo "======================================"
echo "✓ Database setup complete!"
echo "======================================"
echo ""
echo "Database: $DB_NAME"
echo "Tables created:"
echo "  - people"
echo "  - conversations"
echo "  - action_items"
echo ""
echo "Views created:"
echo "  - people_summary"
echo "  - recent_conversations"
echo ""
echo "To seed with sample data, run:"
echo "  python seed_data.py"
echo ""
echo "To start the API server, run:"
echo "  ./run.sh"
echo ""
