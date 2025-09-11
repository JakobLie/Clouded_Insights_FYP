# PostgreSQL Docker Compose Setup
This repository contains a Docker Compose configuration to run a PostgreSQL database container. It provides an easy way to set up and use PostgreSQL for development and testing environments.

## Getting Started

### Prerequisites
- Docker Desktop, Docker & Docker Compose (usually bundled together) installed on your machine
[https://www.docker.com/get-started/]
- PGAdmin installed on your machine (for viewing and modifying database) 
[https://www.pgadmin.org/download/]

### Running PostgreSQL with Docker Compose
1. Open Docker Desktop to start the Docker Daemon
2. Navigate to the the project's `~/Backend/` folder containing the `compose.yaml` file in your command line
3. Run the command `docker compose -p cloudedinsights up --build`

### Accessing the Database via PGAdmin
1. Under "Default Workspace" on your left panel, click on "Add New Server"
2. Under "General" fill up "Name" as "Local_PostgreSQL"
3. Under "Connection", fill in the following details:

    | Field             | Value             | 
    | ----------------- | ----------------- | 
    | Host name/address | localhost         | 
    | Port              | 5432              | 
    | Username          | cloudedinsights   |
    | Password          | cloudedinsights   |
    | Save password?    |True               |
4. Click "Save"
5. Access "Query Tool Workspace" on your left panel
6. For "Existing Server", select "Local_PostgreSQL", this should autopopulate the fields
7. Click on "Connect & Open Query Tool"
8. You are now able to run SQL commands on the database to view or modify data
    - For testing purposes, you may use `SELECT * FROM employee;`

## Explanation
### Project Structure
```bash
Backend/
├── database/
    ├── 01-create.sql # creates tables
    └── 02-insert.sql # inserts test data
├── compose.yaml # builds container based on postgresql community image
└── README_DB.md
```
### Database Initialisation
1. Upon your first initialisation of the database, the scripts in `~/Backend/database` will be run in numerical order
    - `01-create.sql` creates the tables
    - `02-insert.sql` loads in test data
    - These scripts will no longer be run after the first initialisation as long as an existing database is detected
2. After being initialised, the database container "local_postgresql" runs under the Compose Stack "cloudedinsights"
3. Data associated with the database is stored in the volume "cloudedinsights_db_data"

## Shutting Down
### Stopping the Container
1. To stop the container, run `docker compose down` while in the directory `~/Backend/`
### Removing the Database
1. If you wish to completely remove the database, you will need to delete the Compose Stack "cloudedinsights" and Volume "cloudedinsights_db_data" in Docker Desktop