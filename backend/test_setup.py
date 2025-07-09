#!/usr/bin/env python3
"""
Test script to verify MuscleVision backend setup
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import mediapipe as mp
        print("✅ MediaPipe imported successfully")
    except ImportError as e:
        print(f"❌ MediaPipe import failed: {e}")
        return False
    
    try:
        from supabase import create_client
        print("✅ Supabase imported successfully")
    except ImportError as e:
        print(f"❌ Supabase import failed: {e}")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
    
    return True

def test_app_imports():
    """Test if app modules can be imported"""
    print("\n🔍 Testing app imports...")
    
    try:
        from app.core.config import settings
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Config module import failed: {e}")
        return False
    
    try:
        from app.services.pose_estimator import PoseEstimator
        print("✅ PoseEstimator imported successfully")
    except ImportError as e:
        print(f"❌ PoseEstimator import failed: {e}")
        return False
    
    try:
        from app.services.muscle_classifier import MuscleClassifier
        print("✅ MuscleClassifier imported successfully")
    except ImportError as e:
        print(f"❌ MuscleClassifier import failed: {e}")
        return False
    
    return True

def test_pose_estimator():
    """Test pose estimator initialization"""
    print("\n🔍 Testing pose estimator...")
    
    try:
        from app.services.pose_estimator import PoseEstimator
        estimator = PoseEstimator()
        print("✅ PoseEstimator initialized successfully")
        return True
    except Exception as e:
        print(f"❌ PoseEstimator initialization failed: {e}")
        return False

def test_muscle_classifier():
    """Test muscle classifier initialization"""
    print("\n🔍 Testing muscle classifier...")
    
    try:
        from app.services.muscle_classifier import MuscleClassifier
        classifier = MuscleClassifier()
        print("✅ MuscleClassifier initialized successfully")
        return True
    except Exception as e:
        print(f"❌ MuscleClassifier initialization failed: {e}")
        return False

def test_directory_structure():
    """Test if required directories exist"""
    print("\n🔍 Testing directory structure...")
    
    required_dirs = [
        "app",
        "app/core",
        "app/routers", 
        "app/services",
        "static",
        "static/session_outputs"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"❌ Directory missing: {dir_path}")
            return False
    
    return True

def test_files():
    """Test if required files exist"""
    print("\n🔍 Testing required files...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "env.example",
        "app/core/config.py",
        "app/core/database.py",
        "app/services/pose_estimator.py",
        "app/services/muscle_classifier.py",
        "app/routers/detection.py",
        "app/routers/auth.py",
        "app/routers/sessions.py"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ File exists: {file_path}")
        else:
            print(f"❌ File missing: {file_path}")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 MuscleVision Backend Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_app_imports,
        test_pose_estimator,
        test_muscle_classifier,
        test_directory_structure,
        test_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"❌ Test failed: {test.__name__}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend setup is complete.")
        print("\nNext steps:")
        print("1. Copy env.example to .env and configure your Supabase credentials")
        print("2. Set up your Supabase database tables (see README.md)")
        print("3. Run: uvicorn main:app --reload")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 