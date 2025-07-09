#!/usr/bin/env python3
"""
MuscleVision Demo Script for Hackathon Presentation
"""

import requests
import json
import time
import base64
from PIL import Image
import numpy as np
import cv2

class MuscleVisionDemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health(self):
        """Test if the API is running"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ API is running!")
                return True
            else:
                print(f"❌ API health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to API: {e}")
            return False
    
    def register_user(self, email="demo@musclevision.com", password="demo123"):
        """Register a demo user"""
        try:
            data = {
                "email": email,
                "password": password,
                "full_name": "Demo User"
            }
            response = self.session.post(f"{self.base_url}/api/auth/register", json=data)
            if response.status_code == 200:
                result = response.json()
                print("✅ User registered successfully!")
                self.token = result.get("access_token")
                return True
            else:
                print(f"❌ Registration failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False
    
    def login_user(self, email="demo@musclevision.com", password="demo123"):
        """Login demo user"""
        try:
            data = {
                "email": email,
                "password": password
            }
            response = self.session.post(f"{self.base_url}/api/auth/login", json=data)
            if response.status_code == 200:
                result = response.json()
                print("✅ User logged in successfully!")
                self.token = result.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                return True
            else:
                print(f"❌ Login failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def create_demo_image(self, pose_type="bicep_curl"):
        """Create a simple demo image for testing"""
        # Create a simple image with a stick figure
        img = np.ones((480, 640, 3), dtype=np.uint8) * 255
        
        if pose_type == "bicep_curl":
            # Draw a simple stick figure doing bicep curl
            # Head
            cv2.circle(img, (320, 100), 30, (0, 0, 0), 2)
            # Body
            cv2.line(img, (320, 130), (320, 250), (0, 0, 0), 2)
            # Arms (bicep curl position)
            cv2.line(img, (320, 150), (280, 200), (0, 0, 0), 2)  # Left arm
            cv2.line(img, (320, 150), (360, 200), (0, 0, 0), 2)  # Right arm
            # Legs
            cv2.line(img, (320, 250), (300, 350), (0, 0, 0), 2)  # Left leg
            cv2.line(img, (320, 250), (340, 350), (0, 0, 0), 2)  # Right leg
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        return f"data:image/jpeg;base64,{img_base64}"
    
    def analyze_pose(self, image_data=None):
        """Analyze a pose using the API"""
        try:
            if image_data is None:
                image_data = self.create_demo_image()
            
            data = {"image": image_data}
            response = self.session.post(f"{self.base_url}/api/detection/analyze-base64", json=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print("🎯 Pose Analysis Results:")
                    print(f"   Muscle: {result.get('muscle', 'N/A')}")
                    print(f"   Exercise: {result.get('exercise', 'N/A')}")
                    print(f"   Form Accuracy: {result.get('form_accuracy', 'N/A')}%")
                    print(f"   Feedback: {result.get('feedback', 'N/A')}")
                    return result
                else:
                    print(f"❌ Analysis failed: {result.get('message', 'Unknown error')}")
                    return None
            else:
                print(f"❌ API request failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return None
    
    def create_session(self, analysis_result):
        """Create a training session"""
        try:
            data = {
                "muscle_group": analysis_result.get("muscle", "unknown"),
                "exercise_type": analysis_result.get("exercise", "unknown"),
                "form_accuracy": analysis_result.get("form_accuracy", 0),
                "feedback": analysis_result.get("feedback", "No feedback"),
                "duration": 300  # 5 minutes
            }
            
            response = self.session.post(f"{self.base_url}/api/sessions/", json=data)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Training session created!")
                return result
            else:
                print(f"❌ Session creation failed: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Session creation error: {e}")
            return None
    
    def get_stats(self):
        """Get user statistics"""
        try:
            response = self.session.get(f"{self.base_url}/api/sessions/stats/summary")
            
            if response.status_code == 200:
                result = response.json()
                stats = result.get("stats", {})
                print("📊 User Statistics:")
                print(f"   Total Sessions: {stats.get('total_sessions', 0)}")
                print(f"   Average Accuracy: {stats.get('average_accuracy', 0)}%")
                print(f"   Total Duration: {stats.get('total_duration', 0)} seconds")
                return stats
            else:
                print(f"❌ Stats request failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Stats error: {e}")
            return None
    
    def run_full_demo(self):
        """Run a complete demo"""
        print("🚀 MuscleVision Backend Demo")
        print("=" * 50)
        
        # Test API health
        if not self.test_health():
            return False
        
        # Try to login, if fails, register
        if not self.login_user():
            print("Attempting to register new user...")
            if not self.register_user():
                return False
            if not self.login_user():
                return False
        
        # Analyze pose
        print("\n🔍 Analyzing pose...")
        analysis_result = self.analyze_pose()
        
        if analysis_result:
            # Create session
            print("\n💾 Creating training session...")
            self.create_session(analysis_result)
            
            # Get stats
            print("\n📈 Getting user statistics...")
            self.get_stats()
            
            print("\n🎉 Demo completed successfully!")
            return True
        else:
            print("\n❌ Demo failed during pose analysis")
            return False

def main():
    """Main demo function"""
    demo = MuscleVisionDemo()
    
    # You can change the base URL for deployed versions
    # demo = MuscleVisionDemo("https://your-deployed-backend.railway.app")
    
    success = demo.run_full_demo()
    
    if success:
        print("\n✅ Demo completed! Ready for hackathon presentation!")
    else:
        print("\n❌ Demo failed. Check your backend setup.")

if __name__ == "__main__":
    main() 