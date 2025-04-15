# Chat PDF Application

A Django application that allows users to chat with PDF documents using vector embeddings and PostgreSQL with pgvector.

## Prerequisites

- Docker
- Docker Compose

## Tech Stack

- Python 3.12
- Django
- PostgreSQL with pgvector
- ChromaDB
- UV package manager (instead of pip)
- pgAdmin

## Getting Started

### Clone the repository

```bash
git clone <repository-url>
cd chat-pdf
```

### Running with Docker Compose

1. Build and start the containers:

```bash
docker compose up --build
```

This will start the following services:
- Django application (http://localhost:8000)
- PostgreSQL with pgvector
- pgAdmin (http://localhost:5050)
- ChromaDB (http://localhost:8080)

### Running Locally (Without Docker)

1. Set up a Python virtual environment (Python 3.12 recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install UV package manager [here](https://docs.astral.sh/uv/getting-started/installation/):

3. Install dependencies:
```bash
uv sync
```

4. Install and configure PostgreSQL:
- Install PostgreSQL 15 or later
- Enable pgvector extension:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```
- Create a database named 'pdf_chat'

5. Set up environment variables in a .env file:
```bash
POSTGRES_DB=your_database_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

6. Run migrations:
```bash
uv run manage.py migrate
```

7. Start the development server:
```bash
uv run manage.py runserver
```

The application will be available at http://localhost:8000

### Note
When running locally, make sure you have:
- PostgreSQL 15+ installed with pgvector extension
- Python 3.12+ installed
- System dependencies for pdf processing (python-magic requirements)
  - On Ubuntu/Debian: `sudo apt-get install libmagic1`
  - On MacOS: `brew install libmagic`
  - On Windows: No additional steps needed


