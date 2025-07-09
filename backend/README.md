# MuscleVision Backend

A FastAPI-based computer vision backend for real-time muscle detection and form analysis, integrated with Supabase for data storage.

## Features

- **Real-time Pose Detection**: Using MediaPipe for accurate pose estimation
- **Muscle Classification**: Identify activated muscle groups from pose data
- **Form Analysis**: Calculate joint angles and provide form feedback
- **Supabase Integration**: Store user data, sessions, and training history
- **JWT Authentication**: Secure user authentication and authorization
- **RESTful API**: Clean, documented API endpoints

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **MediaPipe**: Real-time pose estimation and tracking
- **OpenCV**: Computer vision and image processing
- **Supabase**: Backend-as-a-Service for database and authentication
- **JWT**: JSON Web Tokens for authentication
- **Pydantic**: Data validation and settings management

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── database.py        # Supabase database operations
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── detection.py       # Pose detection endpoints
│   │   └── sessions.py        # Training session management
│   └── services/
│       ├── pose_estimator.py  # Pose estimation service
│       └── muscle_classifier.py # Muscle classification service
├── static/
│   └── session_outputs/       # Generated session images
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
└── env.example               # Environment variables template
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- Supabase account and project
- Git

### 2. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your Supabase credentials
nano .env
```

Required environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Your Supabase anonymous key
- `SECRET_KEY`: JWT secret key (generate a secure random string)

### 4. Supabase Setup

1. Create a new Supabase project
2. Create the following tables:

**Users Table:**
```sql
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  full_name TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Sessions Table:**
```sql
CREATE TABLE sessions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  muscle_group TEXT NOT NULL,
  exercise_type TEXT NOT NULL,
  form_accuracy DECIMAL(5,2) NOT NULL,
  feedback TEXT NOT NULL,
  image_path TEXT,
  duration INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5. Run the Application

```bash
# Development mode
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout user

### Detection Endpoints

- `POST /api/detection/analyze-frame` - Analyze uploaded image
- `POST /api/detection/analyze-base64` - Analyze base64 encoded image
- `GET /api/detection/health` - Health check

### Session Endpoints

- `POST /api/sessions/` - Create new training session
- `GET /api/sessions/` - Get user's training sessions
- `GET /api/sessions/{session_id}` - Get specific session
- `PUT /api/sessions/{session_id}` - Update session
- `DELETE /api/sessions/{session_id}` - Delete session
- `GET /api/sessions/stats/summary` - Get session statistics

### Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## Usage Examples

### Analyze a Pose

```python
import requests
import base64

# Encode image to base64
with open("pose_image.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# Send request
response = requests.post(
    "http://localhost:8000/api/detection/analyze-base64",
    json={"image": f"data:image/jpeg;base64,{encoded_string}"}
)

result = response.json()
print(f"Detected muscle: {result['muscle']}")
print(f"Exercise type: {result['exercise']}")
print(f"Form accuracy: {result['form_accuracy']}%")
print(f"Feedback: {result['feedback']}")
```

### Create a Training Session

```python
import requests

# First, authenticate
login_response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"email": "user@example.com", "password": "password123"}
)

token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Create session
session_data = {
    "muscle_group": "biceps",
    "exercise_type": "bicep_curl",
    "form_accuracy": 85.5,
    "feedback": "Great form! Keep your elbows close to your body.",
    "duration": 300  # 5 minutes
}

response = requests.post(
    "http://localhost:8000/api/sessions/",
    json=session_data,
    headers=headers
)

print(f"Session created: {response.json()}")
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Code Formatting

```bash
# Install formatting tools
pip install black flake8

# Format code
black .

# Check code style
flake8 .
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

- Set `SECRET_KEY` to a secure random string
- Configure `SUPABASE_URL` and `SUPABASE_ANON_KEY`
- Set appropriate CORS origins
- Configure logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License. 