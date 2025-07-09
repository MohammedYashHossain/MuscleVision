from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from typing import Dict, Any
import base64
import io
from PIL import Image
import json
import os
from datetime import datetime

from app.services.pose_estimator import PoseEstimator
from app.services.muscle_classifier import MuscleClassifier
from app.core.database import create_session, get_supabase
from app.core.config import settings

router = APIRouter()

def get_pose_estimator() -> PoseEstimator:
    """Dependency to get pose estimator instance"""
    return PoseEstimator()

def get_muscle_classifier() -> MuscleClassifier:
    """Dependency to get muscle classifier instance"""
    return MuscleClassifier()

@router.post("/analyze-frame")
async def analyze_frame(
    file: UploadFile = File(...),
    pose_estimator: PoseEstimator = Depends(get_pose_estimator),
    muscle_classifier: MuscleClassifier = Depends(get_muscle_classifier)
):
    """
    Analyze a single frame for pose detection and muscle classification
    """
    try:
        # Read and validate image
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Detect pose
        pose_result = pose_estimator.detect_pose(frame)
        
        if not pose_result["success"]:
            return JSONResponse({
                "success": False,
                "message": "No pose detected. Please ensure you are clearly visible in the camera."
            })
        
        # Calculate joint angles
        keypoints = pose_result["keypoints"]
        angles = pose_estimator.calculate_joint_angles(keypoints)
        
        # Classify muscles
        classification_result = muscle_classifier.classify_muscles(keypoints, angles)
        
        if not classification_result["success"]:
            return JSONResponse({
                "success": False,
                "message": "Error in muscle classification"
            })
        
        # Create annotated image
        annotated_frame = pose_estimator.draw_pose(frame, pose_result["landmarks"])
        
        # Save annotated image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"session_{timestamp}.jpg"
        filepath = os.path.join(settings.upload_dir, filename)
        
        os.makedirs(settings.upload_dir, exist_ok=True)
        cv2.imwrite(filepath, annotated_frame)
        
        # Prepare response
        response_data = {
            "success": True,
            "muscle": classification_result["activated_muscles"][0] if classification_result["activated_muscles"] else "None",
            "exercise": classification_result["exercise_type"],
            "form_accuracy": round(classification_result["form_accuracy"], 1),
            "feedback": classification_result["feedback"],
            "angles": angles,
            "image_path": f"/static/{filename}",
            "timestamp": datetime.now().isoformat()
        }
        
        return JSONResponse(response_data)
        
    except Exception as e:
        print(f"Error in analyze_frame: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-base64")
async def analyze_base64(
    data: Dict[str, Any],
    pose_estimator: PoseEstimator = Depends(get_pose_estimator),
    muscle_classifier: MuscleClassifier = Depends(get_muscle_classifier)
):
    """
    Analyze a base64 encoded image for pose detection and muscle classification
    """
    try:
        # Extract base64 image data
        image_data = data.get("image")
        if not image_data:
            raise HTTPException(status_code=400, detail="Image data is required")
        
        # Decode base64 image
        try:
            image_bytes = base64.b64decode(image_data.split(",")[1] if "," in image_data else image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid base64 image data")
        
        if frame is None:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Detect pose
        pose_result = pose_estimator.detect_pose(frame)
        
        if not pose_result["success"]:
            return JSONResponse({
                "success": False,
                "message": "No pose detected. Please ensure you are clearly visible in the camera."
            })
        
        # Calculate joint angles
        keypoints = pose_result["keypoints"]
        angles = pose_estimator.calculate_joint_angles(keypoints)
        
        # Classify muscles
        classification_result = muscle_classifier.classify_muscles(keypoints, angles)
        
        if not classification_result["success"]:
            return JSONResponse({
                "success": False,
                "message": "Error in muscle classification"
            })
        
        # Prepare response
        response_data = {
            "success": True,
            "muscle": classification_result["activated_muscles"][0] if classification_result["activated_muscles"] else "None",
            "exercise": classification_result["exercise_type"],
            "form_accuracy": round(classification_result["form_accuracy"], 1),
            "feedback": classification_result["feedback"],
            "angles": angles,
            "timestamp": datetime.now().isoformat()
        }
        
        return JSONResponse(response_data)
        
    except Exception as e:
        print(f"Error in analyze_base64: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def detection_health():
    """Health check for detection service"""
    return {
        "status": "healthy",
        "service": "detection",
        "timestamp": datetime.now().isoformat()
    } 