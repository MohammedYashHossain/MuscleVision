from supabase import create_client, Client
from app.core.config import settings
import asyncio
from typing import Optional, Dict, Any
import os

# Global Supabase client
supabase: Optional[Client] = None

async def init_supabase():
    """Initialize Supabase connection"""
    global supabase
    try:
        supabase = create_client(settings.supabase_url, settings.supabase_key)
        print("✅ Supabase connection established")
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        raise

def get_supabase() -> Client:
    """Get Supabase client instance"""
    if supabase is None:
        raise Exception("Supabase not initialized")
    return supabase

# Database operations
async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new user in Supabase"""
    client = get_supabase()
    try:
        response = client.table("users").insert(user_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating user: {e}")
        raise

async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    client = get_supabase()
    try:
        response = client.table("users").select("*").eq("id", user_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

async def create_session(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new training session"""
    client = get_supabase()
    try:
        response = client.table("sessions").insert(session_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating session: {e}")
        raise

async def get_user_sessions(user_id: str, limit: int = 10) -> list:
    """Get user's training sessions"""
    client = get_supabase()
    try:
        response = client.table("sessions").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        print(f"Error getting sessions: {e}")
        return []

async def update_session(session_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a training session"""
    client = get_supabase()
    try:
        response = client.table("sessions").update(update_data).eq("id", session_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating session: {e}")
        raise 