#!/bin/bash
# HBnB Database Setup Script
# Executes schema creation and data seeding

DB_PATH="../instance/development.db"

echo "=== HBnB Database Setup ==="
echo ""

# Check if database exists
if [ -f "$DB_PATH" ]; then
    echo "⚠️  Database already exists at $DB_PATH"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
    rm "$DB_PATH"
    echo "✅ Old database removed"
fi

# Create database with schema
echo ""
echo "📋 Creating database schema..."
sqlite3 "$DB_PATH" < schema.sql
echo "✅ Schema created"

# Insert initial data
echo ""
echo "📦 Inserting initial data..."
sqlite3 "$DB_PATH" < seed.sql
echo "✅ Initial data inserted"

# Run verification queries
echo ""
echo "🔍 Running verification queries..."
echo ""
sqlite3 "$DB_PATH" < queries.sql

echo ""
echo "=== Setup Complete ==="
echo "Database created at: $DB_PATH"
echo ""
echo "To run queries manually:"
echo "  sqlite3 $DB_PATH"
echo ""
echo "To run verification queries:"
echo "  sqlite3 $DB_PATH < sql_scripts/queries.sql"
