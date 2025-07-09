from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.core.database import create_session, get_user_sessions, update_session, get_supabase
from app.routers.auth import get_current_user

router = APIRouter()

class SessionCreate(BaseModel):
    muscle_group: str
    exercise_type: str
    form_accuracy: float
    feedback: str
    image_path: Optional[str] = None
    duration: Optional[int] = None  # in seconds

class SessionUpdate(BaseModel):
    muscle_group: Optional[str] = None
    exercise_type: Optional[str] = None
    form_accuracy: Optional[float] = None
    feedback: Optional[str] = None
    image_path: Optional[str] = None
    duration: Optional[int] = None

class SessionResponse(BaseModel):
    id: str
    user_id: str
    muscle_group: str
    exercise_type: str
    form_accuracy: float
    feedback: str
    image_path: Optional[str] = None
    duration: Optional[int] = None
    created_at: datetime

@router.post("/", response_model=Dict[str, Any])
async def create_training_session(
    session_data: SessionCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new training session"""
    try:
        session_info = {
            "user_id": current_user["id"],
            "muscle_group": session_data.muscle_group,
            "exercise_type": session_data.exercise_type,
            "form_accuracy": session_data.form_accuracy,
            "feedback": session_data.feedback,
            "image_path": session_data.image_path,
            "duration": session_data.duration,
            "created_at": datetime.utcnow().isoformat()
        }
        
        session = await create_session(session_info)
        
        return {
            "success": True,
            "session": {
                "id": session["id"],
                "muscle_group": session["muscle_group"],
                "exercise_type": session["exercise_type"],
                "form_accuracy": session["form_accuracy"],
                "feedback": session["feedback"],
                "image_path": session.get("image_path"),
                "duration": session.get("duration"),
                "created_at": session["created_at"]
            }
        }
        
    except Exception as e:
        print(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create session")

@router.get("/", response_model=Dict[str, Any])
async def get_user_sessions_list(
    limit: int = 10,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get user's training sessions"""
    try:
        sessions = await get_user_sessions(current_user["id"], limit)
        
        return {
            "success": True,
            "sessions": sessions,
            "total": len(sessions)
        }
        
    except Exception as e:
        print(f"Error getting sessions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get sessions")

@router.get("/{session_id}", response_model=Dict[str, Any])
async def get_session(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get a specific training session"""
    try:
        # Get session from Supabase
        supabase = get_supabase()
        session_result = supabase.table("sessions").select("*").eq("id", session_id).eq("user_id", current_user["id"]).execute()
        
        if not session_result.data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = session_result.data[0]
        
        return {
            "success": True,
            "session": session
        }
        
    except Exception as e:
        print(f"Error getting session: {e}")
        raise HTTPException(status_code=500, detail="Failed to get session")

@router.put("/{session_id}", response_model=Dict[str, Any])
async def update_training_session(
    session_id: str,
    session_data: SessionUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update a training session"""
    try:
        # Verify session belongs to user
        supabase = get_supabase()
        session_result = supabase.table("sessions").select("*").eq("id", session_id).eq("user_id", current_user["id"]).execute()
        
        if not session_result.data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Prepare update data
        update_data = {}
        if session_data.muscle_group is not None:
            update_data["muscle_group"] = session_data.muscle_group
        if session_data.exercise_type is not None:
            update_data["exercise_type"] = session_data.exercise_type
        if session_data.form_accuracy is not None:
            update_data["form_accuracy"] = session_data.form_accuracy
        if session_data.feedback is not None:
            update_data["feedback"] = session_data.feedback
        if session_data.image_path is not None:
            update_data["image_path"] = session_data.image_path
        if session_data.duration is not None:
            update_data["duration"] = session_data.duration
        
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Update session
        session = await update_session(session_id, update_data)
        
        return {
            "success": True,
            "session": session
        }
        
    except Exception as e:
        print(f"Error updating session: {e}")
        raise HTTPException(status_code=500, detail="Failed to update session")

@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete a training session"""
    try:
        # Verify session belongs to user
        supabase = get_supabase()
        session_result = supabase.table("sessions").select("*").eq("id", session_id).eq("user_id", current_user["id"]).execute()
        
        if not session_result.data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Delete session
        supabase.table("sessions").delete().eq("id", session_id).execute()
        
        return {
            "success": True,
            "message": "Session deleted successfully"
        }
        
    except Exception as e:
        print(f"Error deleting session: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete session")

@router.get("/stats/summary", response_model=Dict[str, Any])
async def get_session_stats(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get user's training session statistics"""
    try:
        # Get all user sessions
        sessions = await get_user_sessions(current_user["id"], limit=1000)
        
        if not sessions:
            return {
                "success": True,
                "stats": {
                    "total_sessions": 0,
                    "average_accuracy": 0,
                    "total_duration": 0,
                    "muscle_groups": {},
                    "exercise_types": {}
                }
            }
        
        # Calculate statistics
        total_sessions = len(sessions)
        total_accuracy = sum(session.get("form_accuracy", 0) for session in sessions)
        average_accuracy = total_accuracy / total_sessions if total_sessions > 0 else 0
        
        total_duration = sum(session.get("duration", 0) for session in sessions)
        
        # Count muscle groups
        muscle_groups = {}
        for session in sessions:
            muscle = session.get("muscle_group", "Unknown")
            muscle_groups[muscle] = muscle_groups.get(muscle, 0) + 1
        
        # Count exercise types
        exercise_types = {}
        for session in sessions:
            exercise = session.get("exercise_type", "Unknown")
            exercise_types[exercise] = exercise_types.get(exercise, 0) + 1
        
        return {
            "success": True,
            "stats": {
                "total_sessions": total_sessions,
                "average_accuracy": round(average_accuracy, 1),
                "total_duration": total_duration,
                "muscle_groups": muscle_groups,
                "exercise_types": exercise_types
            }
        }
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics") 