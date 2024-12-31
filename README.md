# QA Tools Application

A Flask-based web application for QA task management and location mapping.

## Prerequisites

- Docker
- Docker Compose

## Project Structure
```
taski/
├── app.py                 # Main Flask application with all functionality
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── index.html
│   ├── map_template.html
│   └── generowanie_mapy.html
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
└── .dockerignore       # Docker ignore rules
```

## Database Configuration

Before running the application, update the database connection settings in `app.py`:

```python
def get_db_connection():
    return psycopg2.connect(
        dbname='your_db_name',
        user='your_username',
        password='your_password',
        host='your_host'
    )
```

## Running the Application

1. Build the Docker image:
```bash
docker-compose build
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the application at:
```
http://localhost:50001
```

4. To stop the application:
```bash
docker-compose down
```

## Features

1. Task Generator
   - Create QA tasks with customizable parameters
   - Support for multiple task types
   - Batch task generation

2. Map Generator
   - Generate location maps based on phone numbers or IMEI
   - Support for date range filtering
   - Area overlay functionality
   - Multiple location types (GPS, GSM, WIFI, etc.)

## Notes

- The application runs on port 50001 by default
- Make sure to update database credentials before running
- All data is stored in the configured PostgreSQL database 