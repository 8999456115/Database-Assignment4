#!/bin/bash

echo "🚀 Starting Database Assignment 4 Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Start MySQL container
echo "📦 Starting MySQL container..."
docker run -d \
    --name database-assignment4-db-1 \
    -e MYSQL_ROOT_PASSWORD=rootpass \
    -e MYSQL_DATABASE=subscribers \
    -e MYSQL_USER=subuser \
    -e MYSQL_PASSWORD=subpass \
    -p 3306:3306 \
    mysql:8.0

# Wait for MySQL to be ready
echo "⏳ Waiting for MySQL to be ready..."
timeout 60 bash -c 'until docker exec database-assignment4-db-1 mysqladmin ping -h localhost -u root -prootpass --silent; do sleep 1; done'

if [ $? -eq 0 ]; then
    echo "✅ MySQL is ready!"
    
    # Run initial Flyway migrations
    echo "🔄 Running initial Flyway migrations..."
    docker run --rm \
        --network container:database-assignment4-db-1 \
        -v "$(pwd)/migrations/init:/flyway/sql" \
        -v "$(pwd)/flyway.conf:/flyway/conf/flyway.conf" \
        flyway/flyway:9-alpine migrate
    
    # Run incremental Flyway migrations
    echo "🔄 Running incremental Flyway migrations..."
    docker run --rm \
        --network container:database-assignment4-db-1 \
        -v "$(pwd)/migrations/incremental:/flyway/sql" \
        -v "$(pwd)/flyway_incremental.conf:/flyway/conf/flyway.conf" \
        flyway/flyway:9-alpine migrate
    
    echo "✅ Environment setup complete!"
    echo "📊 Database: subscribers"
    echo "👤 User: subuser"
    echo "🔑 Password: subpass"
    echo "🌐 Host: localhost:3306"
    
else
    echo "❌ MySQL failed to start within timeout"
    exit 1
fi 