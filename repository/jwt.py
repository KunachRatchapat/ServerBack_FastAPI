from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError
import os
from dotenv import load_dotenv


load_dotenv()   

SECRET_KEY: str = os.getenv("SECRET_KEY") # type: ignore
ALGORITHM: str  = os.getenv("JWT_ALGORITHM") # type: ignore
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "43830"))

# --- Protect SECRET_KEY ---
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in environment variables")

class JWTRepo:
    @staticmethod
    def generate_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        
        
        to_encode.update({"exp": expire}) 
        
        
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        try:
           
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        
        except JWTError:
            return {}  # ถ้า token หมดอายุ จะ รีเทินค่าว่าง
