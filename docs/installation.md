# Installation and Setup

This guide will help you set up and run the API License service.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- Redis server
- MongoDB (optional, depending on your repository implementation)
- Keycloak server (for authentication)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/your-organization/api-license.git
cd api-license
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Environment

Create a `.env` file in the root directory with the following variables (adjust as needed):

```
# API Configuration
API_NAME=api-license
API_TAG_NAME=license

# Keycloak Configuration
KEYCLOAK_HOST=https://your-keycloak-server.com
KEYCLOAK_REALM=your-realm
KEYCLOAK_CLIENT_ID=your-client-id
KEYCLOAK_CLIENT_SECRET=your-client-secret

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# MongoDB Configuration (if using MongoDB)
MONGO_URI=mongodb://localhost:27017
MONGO_DB=license_db
```

### 5. Run the API

For development:

```bash
uvicorn main:app --reload
```

For production:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## Docker Deployment

The API can also be deployed using Docker.

### Build the Docker Image

```bash
docker build -t api-license .
```

### Run the Docker Container

```bash
docker run -d -p 8000:8000 \
  -e KEYCLOAK_HOST=https://your-keycloak-server.com \
  -e KEYCLOAK_REALM=your-realm \
  -e KEYCLOAK_CLIENT_ID=your-client-id \
  -e KEYCLOAK_CLIENT_SECRET=your-client-secret \
  -e REDIS_HOST=your-redis-host \
  -e REDIS_PORT=6379 \
  -e REDIS_DB=0 \
  -e REDIS_PASSWORD=your-redis-password \
  --name api-license api-license
```

## API Documentation

Once the API is running, you can access the OpenAPI documentation at:

```
http://localhost:8000/docs
```

And the ReDoc documentation at:

```
http://localhost:8000/redoc
```

## Building the Documentation

To build and serve the documentation locally:

```bash
mkdocs serve
```

This will start a development server at `http://localhost:8000` where you can view the documentation.

To build the documentation for production:

```bash
mkdocs build
```

This will create a `site` directory with the static HTML documentation.

## Troubleshooting

### Common Issues

1. **Connection to Redis fails**:
   - Ensure Redis is running
   - Check the Redis connection parameters in your environment variables

2. **Keycloak authentication fails**:
   - Verify your Keycloak configuration
   - Ensure the client has the correct permissions

3. **API returns 500 errors**:
   - Check the logs for detailed error messages
   - Verify all required environment variables are set correctly

For more help, please open an issue on the repository.