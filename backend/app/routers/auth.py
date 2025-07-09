from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

from app.core.database import create_user, get_user_by_id, get_supabase
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    created_at: datetime

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current user from JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

@router.post("/register", response_model=Dict[str, Any])
async def register(user_data: UserCreate):
    """Register a new user"""
    try:
        # Check if user already exists
        supabase = get_supabase()
        existing_user = supabase.table("users").select("*").eq("email", user_data.email).execute()
        
        if existing_user.data:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user in Supabase
        user_info = {
            "email": user_data.email,
            "password_hash": hashed_password,
            "full_name": user_data.full_name,
            "created_at": datetime.utcnow().isoformat()
        }
        
        user = await create_user(user_info)
        
        # Create access token
        access_token = create_access_token(data={"sub": user["id"]})
        
        return {
            "success": True,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"]
            },
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        print(f"Error in registration: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login", response_model=Dict[str, Any])
async def login(user_credentials: UserLogin):
    """Login user"""
    try:
        # Get user from Supabase
        supabase = get_supabase()
        user_result = supabase.table("users").select("*").eq("email", user_credentials.email).execute()
        
        if not user_result.data:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user = user_result.data[0]
        
        # Verify password
        if not verify_password(user_credentials.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Create access token
        access_token = create_access_token(data={"sub": user["id"]})
        
        return {
            "success": True,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "full_name": user.get("full_name")
            },
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        print(f"Error in login: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.get("/me", response_model=Dict[str, Any])
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user information"""
    return {
        "success": True,
        "user": {
            "id": current_user["id"],
            "email": current_user["email"],
            "full_name": current_user.get("full_name"),
            "created_at": current_user.get("created_at")
        }
    }

@router.post("/logout")
async def logout():
    """Logout user (client-side token removal)"""
    return {
        "success": True,
        "message": "Successfully logged out"
    } 