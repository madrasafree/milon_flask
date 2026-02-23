# Madrasa Spoken Arabic Dictionary (Flask Version)

This repository contains a Flask-based version of the Madrasa Spoken Arabic Dictionary, containerized with Docker for easy setup and development. It serves as a proof-of-concept for migrating the original ASP Classic application to a modern Python web framework.

## Key Features

- **Word Search**: Search for words and view detailed results.
- **Label-Based Browsing**: Explore words by category/label.
- **Word Lists**: View and manage public word lists.
- **User Authentication**: Basic login/logout functionality.
- **Dockerized Environment**: Fully containerized with Docker Compose for one-command setup.

## Tech Stack

- **Backend**: Python 3.12 with Flask
- **Database**: PostgreSQL 16.3
- **Containerization**: Docker & Docker Compose
- **Data Access**: SQLAlchemy

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/madrasafree/milon_flask.git
cd milon_flask
```

### 2. Start the Application

This single command will build the Docker images for the Flask application and the PostgreSQL database, start the containers, and begin loading the database dumps.

```bash
docker compose up --build -d
```

### 3. Monitor Database Setup

The database container will automatically load several large dump files. This process can take a few minutes. To monitor the progress:

```bash
docker compose logs -f db
```

Look for the final message `dump load done`, which indicates that the database is ready.

### 4. Access the Application

Once the database is ready, the application will be available at **http://127.0.0.1:5431/**.

## Architecture

### Services

The `docker-compose.yml` file defines two services:

- **`milon`**: The Flask application container.
  - Builds from the root `Dockerfile`.
  - Runs on port `5431`.
  - Depends on the `db` service.
- **`db`**: The PostgreSQL database container.
  - Builds from the `db_docker/` directory.
  - Exposes the database on port `5432`.
  - Uses a persistent volume (`db_data`) to store data.

### Data Flow

1. On the first run, the `db` container is built.
2. The `db_docker/docker-entrypoint.sh` script starts PostgreSQL and then runs `load_dumps.sh`.
3. `load_dumps.sh` uses `psql` to load the `.sql` dump files located in `db_docker/db_dumps/` into the database.
4. The `milon` (Flask) container starts and connects to the `db` service using the hostname `db`.
5. The Flask application serves requests from the user, querying the PostgreSQL database via SQLAlchemy.

### Project Structure

```
milon_flask/
├── db_docker/             # Configuration for the PostgreSQL container
│   ├── db_dumps/          # SQL dump files for initial data
│   ├── Dockerfile         # Dockerfile for the DB service
│   └── docker-entrypoint.sh # Script to initialize the DB
├── source/                # Flask application source code
│   ├── build/             # DB model definitions (SQLAlchemy)
│   ├── library/           # Helper functions
│   ├── static/            # Static assets (CSS, JS, images)
│   ├── templates/         # Jinja2 HTML templates
│   └── main.py            # Main Flask application file and routes
├── docker-compose.yml     # Defines the services, networks, and volumes
├── Dockerfile             # Dockerfile for the Flask application
└── readme.md              # This file
```

## Key Endpoints

The main application logic is in `source/main.py`. Key routes include:

- `/` or `/default.asp`: Home page with search.
- `/word.asp`: Displays a single word.
- `/labels.asp`: Shows the label cloud.
- `/label.asp`: Shows words for a specific label.
- `/lists.all.asp`: Displays all public word lists.
- `/login.asp` & `/logout`: User authentication.

## Known Issues

- **DB Entrypoint Logic**: The `docker-entrypoint.sh` script in the `db_docker` service has a logic flaw where it checks for the existence of the `public` schema to decide whether to load dumps. Since this schema always exists in PostgreSQL, the dumps are only loaded on the very first volume creation. If the database is cleared but the volume persists, the dumps will not be reloaded automatically. A manual intervention is required in such cases.

## License

This project is licensed under the MIT License.
