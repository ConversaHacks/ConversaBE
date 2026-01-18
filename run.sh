#!/bin/bash

# Start the Conversa Backend API server

echo "Starting Conversa Backend API..."
echo "================================"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Swagger UI: http://localhost:8000/docs"
echo "ReDoc: http://localhost:8000/redoc"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
