import cv2
import numpy as np
import mediapipe as mp
from typing import List, Dict, Any, Optional, Tuple
import json
import os

class PoseEstimator:
    def __init__(self):
        """Initialize pose estimation with MediaPipe as fallback"""
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
    def detect_pose(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Detect pose keypoints in the given frame
        
        Args:
            frame: Input image as numpy array
            
        Returns:
            Dictionary containing keypoints and confidence scores
        """
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame
            results = self.pose.process(rgb_frame)
            
            if results.pose_landmarks:
                keypoints = self._extract_keypoints(results.pose_landmarks, frame.shape)
                return {
                    "success": True,
                    "keypoints": keypoints,
                    "landmarks": results.pose_landmarks
                }
            else:
                return {
                    "success": False,
                    "keypoints": None,
                    "landmarks": None
                }
                
        except Exception as e:
            print(f"Error in pose detection: {e}")
            return {
                "success": False,
                "keypoints": None,
                "landmarks": None,
                "error": str(e)
            }
    
    def _extract_keypoints(self, landmarks, frame_shape: Tuple[int, int, int]) -> List[Dict[str, Any]]:
        """Extract keypoints from MediaPipe landmarks"""
        keypoints = []
        height, width = frame_shape[:2]
        
        for i, landmark in enumerate(landmarks.landmark):
            keypoint = {
                "id": i,
                "x": landmark.x * width,
                "y": landmark.y * height,
                "z": landmark.z,
                "visibility": landmark.visibility
            }
            keypoints.append(keypoint)
            
        return keypoints
    
    def draw_pose(self, frame: np.ndarray, landmarks) -> np.ndarray:
        """Draw pose landmarks on the frame"""
        if landmarks:
            annotated_frame = frame.copy()
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
            return annotated_frame
        return frame
    
    def calculate_joint_angles(self, keypoints: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate joint angles from keypoints"""
        angles = {}
        
        if len(keypoints) < 33:  # MediaPipe pose has 33 landmarks
            return angles
            
        # Define joint connections for angle calculation
        joint_connections = {
            "left_shoulder": [11, 12, 14],  # left shoulder, right shoulder, left elbow
            "right_shoulder": [12, 11, 13],  # right shoulder, left shoulder, right elbow
            "left_elbow": [11, 13, 15],      # left shoulder, left elbow, left wrist
            "right_elbow": [12, 14, 16],     # right shoulder, right elbow, right wrist
            "left_hip": [23, 11, 25],        # left hip, left shoulder, left knee
            "right_hip": [24, 12, 26],       # right hip, right shoulder, right knee
            "left_knee": [23, 25, 27],       # left hip, left knee, left ankle
            "right_knee": [24, 26, 28]       # right hip, right knee, right ankle
        }
        
        for joint_name, joint_indices in joint_connections.items():
            if all(idx < len(keypoints) for idx in joint_indices):
                angle = self._calculate_angle(
                    keypoints[joint_indices[0]],
                    keypoints[joint_indices[1]],
                    keypoints[joint_indices[2]]
                )
                angles[joint_name] = angle
                
        return angles
    
    def _calculate_angle(self, point1: Dict[str, Any], point2: Dict[str, Any], point3: Dict[str, Any]) -> float:
        """Calculate angle between three points"""
        try:
            # Convert to numpy arrays
            a = np.array([point1["x"], point1["y"]])
            b = np.array([point2["x"], point2["y"]])
            c = np.array([point3["x"], point3["y"]])
            
            # Calculate vectors
            ba = a - b
            bc = c - b
            
            # Calculate angle
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
            
            return np.degrees(angle)
        except Exception as e:
            print(f"Error calculating angle: {e}")
            return 0.0 