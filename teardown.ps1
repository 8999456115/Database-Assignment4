Write-Host "Stopping Database Assignment 4 Environment..." -ForegroundColor Yellow

# Stop and remove MySQL container
Write-Host "Stopping MySQL container..." -ForegroundColor Yellow
try {
    docker stop database-assignment4-db-1 2>$null
    docker rm database-assignment4-db-1 2>$null
} catch {
    # Container might not exist, which is fine
}

Write-Host "Environment stopped and cleaned up!" -ForegroundColor Green 