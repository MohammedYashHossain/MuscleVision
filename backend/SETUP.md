# MuscleVision Backend Setup Guide

This guide will help you set up the MuscleVision backend with Supabase integration for computer vision-based muscle detection and form analysis.

## Prerequisites

- Python 3.8 or higher
- Git
- Supabase account (free tier available)
- Docker (optional, for containerized deployment)

## Quick Start (Docker)

If you prefer using Docker, this is the fastest way to get started:

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd backend

# 2. Copy environment template
cp env.example .env

# 3. Edit .env with your Supabase credentials
# (See Supabase Setup section below)

# 4. Run with Docker Compose
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## Manual Setup

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Supabase Setup

#### Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login and create a new project
3. Wait for the project to be ready
4. Go to Settings > API to get your credentials

#### Configure Environment Variables

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your credentials
nano .env
```

Update the following variables:
```env
SUPABASE_URL=https://rxnsdoffxuqjfdkwzplo.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bnNkb2ZmeHVxamZka3d6cGxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwODUyMTAsImV4cCI6MjA2NzY2MTIxMH0.4vgyfR0qk4cmz3QjX-OXuzdD4YehgXL2gEOUakNge8A
SECRET_KEY=musclevision-secret-key-2024-change-this-in-production
API_HOST=0.0.0.0
API_PORT=8000
UPLOAD_DIR=static/session_outputs
MAX_FILE_SIZE=10485760
POSE_MODEL_PATH=models/mmpose_hrnet_w48_coco_256x192
CONFIDENCE_THRESHOLD=0.5
```

#### Create Database Tables

Run these SQL commands in your Supabase SQL Editor:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  full_name TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sessions table
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

-- Create indexes for better performance
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_created_at ON sessions(created_at DESC);
CREATE INDEX idx_users_email ON users(email);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own profile" ON users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view own sessions" ON sessions
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own sessions" ON sessions
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own sessions" ON sessions
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own sessions" ON sessions
  FOR DELETE USING (auth.uid() = user_id);
```

### 3. Test Setup

```bash
# Run the test script to verify everything is working
python test_setup.py
```

You should see all tests passing. If any fail, check the error messages and ensure all dependencies are installed.

### 4. Run the Application

```bash
# Development mode (with auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5. Verify Installation

Visit `http://localhost:8000/docs` to see the interactive API documentation.

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Detection
- `POST /api/detection/analyze-frame` - Analyze uploaded image
- `POST /api/detection/analyze-base64` - Analyze base64 image
- `GET /api/detection/health` - Health check

### Sessions
- `POST /api/sessions/` - Create training session
- `GET /api/sessions/` - Get user sessions
- `GET /api/sessions/stats/summary` - Get statistics

## Testing the API

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Save the `access_token` from the response.

### 3. Test Pose Detection

```bash
# Using base64 image (replace with your image)
curl -X POST "http://localhost:8000/api/detection/analyze-base64" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
  }'
```

### 4. Create a Session

```bash
curl -X POST "http://localhost:8000/api/sessions/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "muscle_group": "biceps",
    "exercise_type": "bicep_curl",
    "form_accuracy": 85.5,
    "feedback": "Great form!",
    "duration": 300
  }'
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Supabase Connection Errors**: Verify your credentials in `.env`

3. **Permission Errors**: Ensure the `static/session_outputs` directory is writable

4. **Port Already in Use**: Change the port in the uvicorn command
   ```bash
   uvicorn main:app --reload --port 8001
   ```

### Logs

Check the application logs for detailed error information:
```bash
# If using Docker
docker-compose logs musclevision-backend

# If running directly
# Logs will appear in the terminal
```

## Production Deployment

### Environment Variables

For production, ensure these environment variables are set:
- `SECRET_KEY`: Use a strong, random secret key
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Your Supabase anonymous key

### Security Considerations

1. Use HTTPS in production
2. Set appropriate CORS origins
3. Use environment variables for sensitive data
4. Enable Supabase Row Level Security
5. Implement rate limiting

### Scaling

The backend is designed to be stateless and can be scaled horizontally:
- Use a load balancer
- Consider using Redis for session storage
- Use a CDN for static files

## Support

If you encounter issues:
1. Check the logs for error messages
2. Verify your Supabase setup
3. Ensure all dependencies are installed
4. Check the API documentation at `/docs`

For additional help, refer to the main README.md file. 