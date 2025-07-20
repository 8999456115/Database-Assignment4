Write-Host "Starting Database Assignment 4 Environment..." -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Start MySQL container
Write-Host "Starting MySQL container..." -ForegroundColor Yellow
docker run -d `
    --name database-assignment4-db-1 `
    -e MYSQL_ROOT_PASSWORD=rootpass `
    -e MYSQL_DATABASE=subscribers `
    -e MYSQL_USER=subuser `
    -e MYSQL_PASSWORD=subpass `
    -p 3306:3306 `
    mysql:8.0

# Wait for MySQL to be ready
Write-Host "Waiting for MySQL to be ready..." -ForegroundColor Yellow
$timeout = 60
$elapsed = 0
$ready = $false

while ($elapsed -lt $timeout -and -not $ready) {
    try {
        docker exec database-assignment4-db-1 mysqladmin ping -h localhost -u root -prootpass --silent | Out-Null
        $ready = $true
    } catch {
        Start-Sleep -Seconds 1
        $elapsed++
    }
}

if ($ready) {
    Write-Host "MySQL is ready!" -ForegroundColor Green
    
    # Run initial Flyway migrations
    Write-Host "Running initial Flyway migrations..." -ForegroundColor Yellow
    docker run --rm `
        --network container:database-assignment4-db-1 `
        -v "${PWD}/migrations/init:/flyway/sql" `
        -v "${PWD}/flyway.conf:/flyway/conf/flyway.conf" `
        flyway/flyway:9-alpine migrate
    
    # Run incremental Flyway migrations
    Write-Host "Running incremental Flyway migrations..." -ForegroundColor Yellow
    docker run --rm `
        --network container:database-assignment4-db-1 `
        -v "${PWD}/migrations/incremental:/flyway/sql" `
        -v "${PWD}/flyway_incremental.conf:/flyway/conf/flyway.conf" `
        flyway/flyway:9-alpine migrate
    
    Write-Host "Environment setup complete!" -ForegroundColor Green
    Write-Host "Database: subscribers" -ForegroundColor Cyan
    Write-Host "User: subuser" -ForegroundColor Cyan
    Write-Host "Password: subpass" -ForegroundColor Cyan
    Write-Host "Host: localhost:3306" -ForegroundColor Cyan
    
} else {
    Write-Host "MySQL failed to start within timeout" -ForegroundColor Red
    exit 1
} 