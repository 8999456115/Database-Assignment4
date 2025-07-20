<<<<<<< HEAD
# Database Assignment 4 - Flyway Migration System

This project implements a complete database migration system using Flyway, Ansible, and GitHub Actions for managing a subscribers database.

## Project Structure

```
Database-Assignment4-main/
├── .github/workflows/          # GitHub Actions workflows
├── migrations/
│   ├── init/                   # Initial database schema
│   │   └── V1__init_schema.sql
│   └── incremental/            # Incremental migrations
│       └── V2__add_name_column.sql
├── up.yml                      # Ansible playbook to scaffold environment
├── down.yml                    # Ansible playbook to remove environment
├── flyway.conf                 # Flyway configuration for initial migrations
├── flyway_incremental.conf     # Flyway configuration for incremental migrations
├── test_subscribers.py         # Automated CRUD tests
└── README.md                   # This file
```

## Prerequisites

- Docker
- Ansible
- Python 3.7+
- MySQL client (optional, for manual testing)

## Quick Start

### Method 1: Using Ansible (Recommended)

#### 1. Start the Environment

```bash
# Start MySQL container and run initial migrations
ansible-playbook up.yml
```

This will:
- Start a MySQL 8.0 container
- Create the `subscribers` database
- Create user `subuser` with password `subpass`
- Run initial Flyway migrations using nektos/act

#### 2. Stop the Environment

```bash
# Stop and remove the MySQL container
ansible-playbook down.yml
```

### Method 2: Using Docker Compose

#### 1. Start the Environment

```bash
# Start MySQL container
docker-compose up -d

# Wait for MySQL to be ready, then run migrations
./setup.sh
```

#### 2. Stop the Environment

```bash
# Stop and remove containers
docker-compose down
```

### Method 3: Manual Setup

#### 1. Start the Environment

**Linux/macOS:**
```bash
# Run the setup script
./setup.sh
```

**Windows PowerShell:**
```powershell
# Run the setup script
.\setup.ps1
```

#### 2. Stop the Environment

**Linux/macOS:**
```bash
# Run the teardown script
./teardown.sh
```

**Windows PowerShell:**
```powershell
# Run the teardown script
.\teardown.ps1
```

### Run Tests Locally

```bash
# Install Python dependencies
pip install mysql-connector-python

# Test database connection
python test_connection.py

# Run the automated tests
python test_subscribers.py
```

## Database Schema

### Initial Schema (V1__init_schema.sql)
```sql
CREATE TABLE IF NOT EXISTS subscriber (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE
);
```

### Incremental Migration (V2__add_name_column.sql)
```sql
ALTER TABLE subscriber ADD COLUMN name VARCHAR(255);
```

## Migration System

### Initial Migrations
- Located in `migrations/init/`
- Configured in `flyway.conf`
- Creates the base database schema

### Incremental Migrations
- Located in `migrations/incremental/`
- Configured in `flyway_incremental.conf`
- Applied after initial migrations for schema evolution

## GitHub Actions Workflow

The workflow (`.github/workflows/flyway.yml`) automatically:

1. **Starts MySQL Container**: Creates a fresh MySQL instance
2. **Runs Initial Migrations**: Applies base schema using Flyway
3. **Runs Incremental Migrations**: Applies schema changes using Flyway
4. **Executes Tests**: Runs comprehensive CRUD tests
5. **Reports Deployment**: Outputs deployment status
6. **Cleanup**: Removes containers after completion

### Manual Workflow Trigger

```bash
# Run GitHub Actions locally using nektos/act
act -W .github/workflows/flyway.yml --env-file .env
```

## Automated Testing

The test suite (`test_subscribers.py`) includes comprehensive CRUD operations:

- **Create**: Test subscriber creation
- **Read**: Test data retrieval
- **Update**: Test data modification
- **Delete**: Test subscriber removal
- **Constraints**: Test unique email constraint
- **Listing**: Test retrieving multiple subscribers

Each test manages its own data and cleans up after execution.

## Environment Variables

Create a `.env` file with the following variables:

```env
DB_HOST=localhost
DB_USER=subuser
DB_PASSWORD=subpass
DB_NAME=subscribers
```

## Manual Database Access

```bash
# Connect to MySQL
mysql -h localhost -u subuser -psubpass subscribers

# Or as root
mysql -h localhost -u root -prootpass subscribers
```

## Troubleshooting

### MySQL Connection Issues
If you encounter connection errors:
1. Ensure Docker is running
2. Check if the container is started: `docker ps`
3. Wait for MySQL to be ready (up.yml includes a wait step)
4. Verify environment variables in `.env` file

### Flyway Migration Issues
1. Check Flyway configuration files
2. Ensure migration files follow naming convention: `V{version}__{description}.sql`
3. Verify database connection settings

### Test Failures
1. Ensure MySQL container is running
2. Check database connection parameters
3. Verify table schema matches test expectations

## Assignment Requirements Met

✅ **Up and Down YAML files** - `up.yml` and `down.yml` for environment management  
✅ **Initial Setup** - Migrations folder and Flyway commands for subscriber database  
✅ **Incremental Migrations** - Separate migrations folder for schema evolution  
✅ **GitHub Actions Workflow** - Automated pipeline running both migration sets  
✅ **Automated Tests** - Comprehensive CRUD tests with self-managed data  
✅ **Deployment Indicator** - Console output showing deployment completion  
✅ **README Documentation** - Complete instructions for reproduction  

## Repository Link

[Link to your repository here]

## PDF Submission

[Attach your PDF with answers to Question 1 here]
=======
# PROG8850Week1Installation
install mysql, python

```bash
ansible-playbook up.yml
```

To use mysql:

```bash
mysql -u root -h 127.0.0.1 -p
```

To run github actions like (notice that the environment variables default for the local case):

```yaml
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Install MySQL client
        run: sudo apt-get update && sudo apt-get install -y mysql-client

      - name: Deploy to Database
        env:
          DB_HOST: ${{ secrets.DB_HOST || '127.0.0.1' }} 
          DB_USER: ${{ secrets.DB_ADMIN_USER || 'root' }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD  || 'Secret5555'}}
          DB_NAME: ${{ secrets.DB_NAME || 'mysql' }}
        run: mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME < schema_changes.sql
```

locally:

first try

```bash
bin/act
```

then if that doesn't work 

```bash
bin/act -P ubuntu-latest=-self-hosted
```

to run in the codespace.

To shut down:

```bash
ansible-playbook down.yml
```

There is also a flyway migration here. To run the migration:

```bash
docker run --rm -v "/workspaces/<repo name>/migrations:/flyway/sql" redgate/flyway -user=root -password=Secret5555 -url=jdbc:mysql://172.17.0.1:3306/flyway_test migrate
```

This is a reproducible mysql setup, with a flyway migration. It is also the start of an example of using flyway and github actions together. Flyway (jdbc) needs the database to exist. The github action creates it if it doesn't exist and flyway takes over from there.
>>>>>>> f7444b639cdd3cfdaccd957c0f01d62b7dce86e0
