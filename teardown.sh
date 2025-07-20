#!/bin/bash

echo "🛑 Stopping Database Assignment 4 Environment..."

# Stop and remove MySQL container
echo "📦 Stopping MySQL container..."
docker stop database-assignment4-db-1 2>/dev/null || true
docker rm database-assignment4-db-1 2>/dev/null || true

echo "✅ Environment stopped and cleaned up!" 