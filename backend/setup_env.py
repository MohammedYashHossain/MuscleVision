"""
Script to set up environment variables for MuscleVision backend
"""

import os

def create_env_file():
    """Create .env file with Supabase credentials"""
    
    env_content = """# Supabase Configuration
SUPABASE_URL=https://rxnsdoffxuqjfdkwzplo.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bnNkb2ZmeHVxamZka3d6cGxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwODUyMTAsImV4cCI6MjA2NzY2MTIxMH0.4vgyfR0qk4cmz3QjX-OXuzdD4YehgXL2gEOUakNge8A

# JWT Configuration
SECRET_KEY=musclevision-secret-key-2024-change-this-in-production

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# File Upload Configuration
UPLOAD_DIR=static/session_outputs
MAX_FILE_SIZE=10485760

# Model Configuration
POSE_MODEL_PATH=models/mmpose_hrnet_w48_coco_256x192
CONFIDENCE_THRESHOLD=0.5
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 Environment variables configured with your Supabase credentials")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_supabase_connection():
    """Test connection to Supabase"""
    try:
        from supabase import create_client
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        # Get credentials
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Supabase credentials not found in .env file")
            return False
        
        # Test connection
        supabase = create_client(supabase_url, supabase_key)
        
        # Try a simple query to test connection
        response = supabase.table("users").select("count", count="exact").execute()
        
        print("✅ Supabase connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 MuscleVision Backend Environment Setup")
    print("=" * 50)
    
    # Create .env file
    if create_env_file():
        print("\n🔍 Testing Supabase connection...")
        if test_supabase_connection():
            print("\n🎉 Environment setup complete!")
            print("\nNext steps:")
            print("1. Set up Supabase database tables (see SETUP.md)")
            print("2. Install dependencies: pip install -r requirements.txt")
            print("3. Run the backend: uvicorn main:app --reload")
        else:
            print("\n⚠️  Supabase connection failed. Please check your credentials.")
    else:
        print("\n❌ Failed to create .env file")

if __name__ == "__main__":
    main() 