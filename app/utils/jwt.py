from jwt import encode, decode
from datetime import datetime, timezone, timedelta
from app.env import SECRET_KEY

def create_jwt_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    
    return encode(payload=payload, key=SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token):
    try:
        payload = decode(token, SECRET_KEY, algorithms="HS256")
        exp = payload.get("exp")
        user_id = payload.get("user_id")
        
        if not exp or not user_id:
            return None
        
        now = datetime.now(timezone.utc).timestamp()
        
        if now > exp:
            return None
        
        return user_id
    except:
        return None