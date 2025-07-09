import numpy as np
from typing import List, Dict, Any, Optional
import json

class MuscleClassifier:
    def __init__(self):
        """Initialize muscle classification with exercise patterns"""
        self.exercise_patterns = self._load_exercise_patterns()
        self.muscle_groups = {
            "biceps": ["left_elbow", "right_elbow"],
            "triceps": ["left_elbow", "right_elbow"],
            "shoulders": ["left_shoulder", "right_shoulder"],
            "chest": ["left_shoulder", "right_shoulder"],
            "back": ["left_shoulder", "right_shoulder"],
            "quads": ["left_knee", "right_knee"],
            "hamstrings": ["left_knee", "right_knee"],
            "calves": ["left_knee", "right_knee"],
            "abs": ["left_hip", "right_hip"]
        }
        
    def _load_exercise_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load exercise patterns and their characteristics"""
        return {
            "bicep_curl": {
                "muscles": ["biceps"],
                "angle_ranges": {
                    "left_elbow": (30, 160),
                    "right_elbow": (30, 160)
                },
                "movement_pattern": "flexion",
                "description": "Bicep curl exercise"
            },
            "tricep_extension": {
                "muscles": ["triceps"],
                "angle_ranges": {
                    "left_elbow": (30, 160),
                    "right_elbow": (30, 160)
                },
                "movement_pattern": "extension",
                "description": "Tricep extension exercise"
            },
            "shoulder_press": {
                "muscles": ["shoulders", "triceps"],
                "angle_ranges": {
                    "left_shoulder": (45, 180),
                    "right_shoulder": (45, 180),
                    "left_elbow": (60, 180),
                    "right_elbow": (60, 180)
                },
                "movement_pattern": "press",
                "description": "Shoulder press exercise"
            },
            "squat": {
                "muscles": ["quads", "hamstrings", "glutes"],
                "angle_ranges": {
                    "left_knee": (60, 180),
                    "right_knee": (60, 180),
                    "left_hip": (45, 180),
                    "right_hip": (45, 180)
                },
                "movement_pattern": "squat",
                "description": "Squat exercise"
            },
            "push_up": {
                "muscles": ["chest", "triceps", "shoulders"],
                "angle_ranges": {
                    "left_elbow": (60, 180),
                    "right_elbow": (60, 180),
                    "left_shoulder": (45, 180),
                    "right_shoulder": (45, 180)
                },
                "movement_pattern": "push",
                "description": "Push-up exercise"
            }
        }
    
    def classify_muscles(self, keypoints: List[Dict[str, Any]], angles: Dict[str, float]) -> Dict[str, Any]:
        """
        Classify activated muscles based on pose keypoints and joint angles
        
        Args:
            keypoints: List of pose keypoints
            angles: Dictionary of joint angles
            
        Returns:
            Dictionary containing muscle classification results
        """
        try:
            # Analyze pose for muscle activation
            activated_muscles = self._analyze_muscle_activation(keypoints, angles)
            
            # Identify exercise type
            exercise_type = self._identify_exercise(angles)
            
            # Calculate form accuracy
            form_accuracy = self._calculate_form_accuracy(exercise_type, angles)
            
            # Generate feedback
            feedback = self._generate_feedback(exercise_type, angles, form_accuracy)
            
            return {
                "success": True,
                "activated_muscles": activated_muscles,
                "exercise_type": exercise_type,
                "form_accuracy": form_accuracy,
                "feedback": feedback,
                "angles": angles
            }
            
        except Exception as e:
            print(f"Error in muscle classification: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _analyze_muscle_activation(self, keypoints: List[Dict[str, Any]], angles: Dict[str, float]) -> List[str]:
        """Analyze which muscles are being activated"""
        activated_muscles = []
        
        # Check for bicep activation (elbow flexion)
        if "left_elbow" in angles and "right_elbow" in angles:
            if angles["left_elbow"] < 90 or angles["right_elbow"] < 90:
                activated_muscles.append("biceps")
        
        # Check for tricep activation (elbow extension)
        if "left_elbow" in angles and "right_elbow" in angles:
            if angles["left_elbow"] > 120 or angles["right_elbow"] > 120:
                activated_muscles.append("triceps")
        
        # Check for shoulder activation
        if "left_shoulder" in angles and "right_shoulder" in angles:
            if angles["left_shoulder"] > 90 or angles["right_shoulder"] > 90:
                activated_muscles.append("shoulders")
        
        # Check for leg muscle activation
        if "left_knee" in angles and "right_knee" in angles:
            if angles["left_knee"] < 120 or angles["right_knee"] < 120:
                activated_muscles.extend(["quads", "hamstrings"])
        
        return list(set(activated_muscles))  # Remove duplicates
    
    def _identify_exercise(self, angles: Dict[str, float]) -> str:
        """Identify the type of exercise being performed"""
        best_match = "unknown"
        best_score = 0
        
        for exercise_name, pattern in self.exercise_patterns.items():
            score = self._calculate_exercise_similarity(pattern, angles)
            if score > best_score:
                best_score = score
                best_match = exercise_name
        
        return best_match if best_score > 0.3 else "unknown"
    
    def _calculate_exercise_similarity(self, pattern: Dict[str, Any], angles: Dict[str, float]) -> float:
        """Calculate similarity between current angles and exercise pattern"""
        score = 0
        total_checks = 0
        
        for joint, angle_range in pattern["angle_ranges"].items():
            if joint in angles:
                min_angle, max_angle = angle_range
                current_angle = angles[joint]
                
                if min_angle <= current_angle <= max_angle:
                    score += 1
                total_checks += 1
        
        return score / total_checks if total_checks > 0 else 0
    
    def _calculate_form_accuracy(self, exercise_type: str, angles: Dict[str, float]) -> float:
        """Calculate form accuracy percentage"""
        if exercise_type == "unknown":
            return 0.0
        
        pattern = self.exercise_patterns.get(exercise_type, {})
        if not pattern:
            return 0.0
        
        accuracy = 0
        total_checks = 0
        
        for joint, angle_range in pattern["angle_ranges"].items():
            if joint in angles:
                min_angle, max_angle = angle_range
                current_angle = angles[joint]
                
                # Calculate how close the angle is to the ideal range
                if min_angle <= current_angle <= max_angle:
                    # Perfect form
                    accuracy += 100
                else:
                    # Calculate deviation penalty
                    if current_angle < min_angle:
                        deviation = min_angle - current_angle
                    else:
                        deviation = current_angle - max_angle
                    
                    penalty = min(deviation * 2, 50)  # Max 50% penalty
                    accuracy += max(100 - penalty, 0)
                
                total_checks += 1
        
        return accuracy / total_checks if total_checks > 0 else 0
    
    def _generate_feedback(self, exercise_type: str, angles: Dict[str, float], accuracy: float) -> str:
        """Generate form feedback based on exercise type and accuracy"""
        if exercise_type == "unknown":
            return "Please position yourself clearly in the camera view."
        
        feedback_messages = []
        
        if accuracy < 70:
            feedback_messages.append("Focus on maintaining proper form.")
        
        if exercise_type == "bicep_curl":
            if "left_elbow" in angles and angles["left_elbow"] > 160:
                feedback_messages.append("Keep your elbows close to your body.")
            if "right_elbow" in angles and angles["right_elbow"] > 160:
                feedback_messages.append("Maintain controlled movement throughout.")
        
        elif exercise_type == "squat":
            if "left_knee" in angles and angles["left_knee"] > 150:
                feedback_messages.append("Go deeper into the squat position.")
            if "right_knee" in angles and angles["right_knee"] > 150:
                feedback_messages.append("Keep your knees aligned with your toes.")
        
        elif exercise_type == "push_up":
            if "left_elbow" in angles and angles["left_elbow"] > 150:
                feedback_messages.append("Lower your body closer to the ground.")
            if "right_elbow" in angles and angles["right_elbow"] > 150:
                feedback_messages.append("Maintain a straight body line.")
        
        if not feedback_messages:
            feedback_messages.append("Great form! Keep it up!")
        
        return " ".join(feedback_messages) 