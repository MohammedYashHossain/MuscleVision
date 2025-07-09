# <h1 align="center">MuscleVision - AI-Powered Fitness Form Analysis</h1>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img alt="React" src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"/>
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi"/>
  <img alt="Supabase" src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white"/>
  <img alt="License" src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge"/>
  <img alt="Repository" src="https://img.shields.io/badge/GitHub-MohammedYashHossain-181717?style=for-the-badge&logo=github"/>
</p>

<p align="center">
  A full-stack computer vision application that uses AI to detect muscle activation, analyze exercise form, and provide real-time feedback. Built with React, FastAPI, MediaPipe, and Supabase.
</p>

---

### Key Features

<table>
<tr>
<td>

#### Computer Vision
- Real-time pose detection
- Muscle activation analysis
- Joint angle calculations
- Form accuracy scoring

</td>
<td>

#### Exercise Recognition
- Bicep curls & tricep extensions
- Shoulder presses & push-ups
- Squats & leg exercises
- Custom exercise patterns

</td>
<td>

#### User Experience
- Live webcam analysis
- Personalized feedback
- Session tracking
- Progress statistics

</td>
</tr>
</table>

### Technical Architecture

<table>
<tr>
<td>

#### Frontend (React)
- Modern UI with Tailwind CSS
- Real-time webcam integration
- Responsive design
- Interactive feedback

</td>
<td>

#### Backend (FastAPI)
- RESTful API design
- Computer vision processing
- Supabase integration
- JWT authentication

</td>
<td>

#### AI/ML Pipeline
- MediaPipe pose estimation
- Custom muscle classification
- Form analysis algorithms
- Real-time processing

</td>
</tr>
</table>

### Technologies

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![React](https://img.shields.io/badge/-React-20232A?style=flat&logo=react&logoColor=61DAFB)
![FastAPI](https://img.shields.io/badge/-FastAPI-005571?style=flat&logo=fastapi)
![MediaPipe](https://img.shields.io/badge/-MediaPipe-4285F4?style=flat&logo=google)
![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?style=flat&logo=opencv)
![Supabase](https://img.shields.io/badge/-Supabase-3ECF8E?style=flat&logo=supabase)
![Tailwind CSS](https://img.shields.io/badge/-Tailwind%20CSS-38B2AC?style=flat&logo=tailwind-css)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?style=flat&logo=typescript)

### Getting Started

#### System Requirements
- Python 3.8 or higher
- Node.js 16 or higher
- Webcam for real-time analysis
- Modern web browser
- Supabase account (free tier available)

#### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/MohammedYashHossain/MuscleVision.git
   cd MuscleVision/muscle-vision
   ```

2. **Set Up Supabase**
   - Create a free account at [supabase.com](https://supabase.com)
   - Create a new project
   - Run the SQL commands from `backend/supabase_setup.sql` in your Supabase SQL Editor
   - Copy your project URL and anon key

3. **Backend Setup**
   ```bash
   cd backend
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Create environment file
   cp env.example .env
   # Edit .env with your Supabase credentials
   ```

4. **Frontend Setup**
   ```bash
   # From the muscle-vision directory
   npm install
   ```

5. **Run the Application**
   ```bash
   # Terminal 1 - Backend (from backend directory)
   uvicorn main:app --reload
   
   # Terminal 2 - Frontend (from muscle-vision directory)
   npm run dev
   ```

6. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

#### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SECRET_KEY=your_jwt_secret_key
```

### API Endpoints

<table>
<tr>
<td>

#### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get user info

</td>
<td>

#### Detection
- `POST /api/detection/analyze-frame` - Upload image analysis
- `POST /api/detection/analyze-base64` - Base64 image analysis
- `GET /api/detection/health` - Health check

</td>
<td>

#### Sessions
- `POST /api/sessions/` - Create training session
- `GET /api/sessions/` - Get user sessions
- `GET /api/sessions/stats/summary` - Get statistics

</td>
</tr>
</table>

### Project Structure

```
MuscleVision/
├── 🎯 muscle-vision/          # React frontend
│   ├── src/
│   │   ├── app/              # Next.js pages
│   │   └── components/       # React components
│   ├── package.json
│   └── README.md
├── ⚙️ backend/               # FastAPI backend
│   ├── app/
│   │   ├── core/            # Configuration & database
│   │   ├── routers/         # API endpoints
│   │   └── services/        # Computer vision services
│   ├── static/              # Generated images
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── README.md           # Backend documentation
└── 📚 docs/                 # Project documentation
```

### Features in Detail

#### Computer Vision Pipeline
- **Pose Detection**: Uses MediaPipe for real-time 33-point pose estimation
- **Joint Analysis**: Calculates angles for elbows, shoulders, knees, and hips
- **Muscle Classification**: Identifies activated muscle groups based on pose data
- **Form Scoring**: Provides accuracy percentages and personalized feedback

#### Exercise Recognition
- **Bicep Curls**: Detects elbow flexion and arm positioning
- **Tricep Extensions**: Analyzes arm extension patterns
- **Shoulder Presses**: Monitors overhead movement and form
- **Squats**: Tracks knee and hip angles for proper depth
- **Push-ups**: Evaluates body alignment and arm positioning

#### User Management
- **Authentication**: Secure JWT-based user authentication
- **Session Tracking**: Stores workout sessions with timestamps
- **Progress Analytics**: Tracks form improvement over time
- **Personalized Feedback**: AI-generated form correction suggestions

### Deployment

#### Backend Deployment (Railway)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy backend
cd backend
railway login
railway init
railway up
```

#### Frontend Deployment (Vercel)
```bash
# Deploy frontend
cd muscle-vision
npm run build
vercel --prod
```

#### Docker Deployment
```bash
# Build and run with Docker Compose
cd backend
docker-compose up --build
```

### Demo

Run the demo script to test the backend functionality:

```bash
cd backend
python demo.py
```

This will:
- Test API connectivity
- Register a demo user
- Analyze a sample pose
- Create a training session
- Display user statistics

### Troubleshooting

#### Common Issues

- **Webcam not working**: Ensure camera permissions are granted
- **Pose detection fails**: Check lighting and ensure full body is visible
- **Supabase connection errors**: Verify credentials in `.env` file
- **Dependencies issues**: Update pip and reinstall requirements

#### Performance Tips

- Use good lighting for better pose detection
- Ensure stable internet connection for real-time analysis
- Close unnecessary applications to free up system resources
- Use modern browsers for optimal webcam performance

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Developer

<p align="center">
  <b>Mohammed Y. Hossain</b><br>
  <a href="https://mohammedyhossain-portfolio.vercel.app/"><img alt="Portfolio" src="https://img.shields.io/badge/Portfolio-View-red?style=flat-square"/></a>
  <a href="https://www.linkedin.com/in/mohammedyhossain/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin"/></a>
  <a href="mailto:mohossain.swe@gmail.com"><img alt="Email" src="https://img.shields.io/badge/Email-Contact-D14836?style=flat-square&logo=gmail&logoColor=white"/></a>
</p>

---

<p align="center">
  <i>This project demonstrates the integration of computer vision, machine learning, and full-stack web development for fitness applications.</i>
</p>
