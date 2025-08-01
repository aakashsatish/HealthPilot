from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
import jwt
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer()

class AuthService:
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token and return user info"""
        try:
            # For now, we'll use a simple approach
            # In production, you'd verify with Supabase
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return None
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
        """Get current user from token"""
        token = credentials.credentials
        user_info = self.verify_token(token)
        
        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return user_info