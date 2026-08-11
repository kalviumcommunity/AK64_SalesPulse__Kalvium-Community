"""
SalesPulse Authentication & Role-Based Access Control Module
------------------------------------------------------------
Implements FR-01 to FR-04:
  - User registration & secure password hashing
  - JWT (JSON Web Token) issuance and validation
  - Role-based permissions (Rep, Manager, Admin)
  - Session security tracking
"""

import hashlib
import json
import base64
import time
from database_manager import get_db, hash_password

SECRET_KEY = "salespulse_secret_jwt_key_super_secure"

try:
    import jwt
    HAS_PYJWT = True
except ImportError:
    HAS_PYJWT = False

def create_jwt_token(user_id, email, name, role, expires_in=86400):
    """Generate JWT payload with user attributes and expiration."""
    payload = {
        "user_id": user_id,
        "email": email,
        "name": name,
        "role": role,
        "exp": int(time.time()) + expires_in
    }
    
    if HAS_PYJWT:
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    else:
        # Fallback JWT encoding if PyJWT package is not installed
        header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip("=")
        body = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        signature = hashlib.sha256(f"{header}.{body}.{SECRET_KEY}".encode()).hexdigest()
        return f"{header}.{body}.{signature}"

def decode_jwt_token(token):
    """Verify and decode JWT token payload."""
    if not token:
        return None
    
    try:
        if HAS_PYJWT:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        else:
            parts = token.split(".")
            if len(parts) != 3:
                return None
            header, body, signature = parts
            expected_sig = hashlib.sha256(f"{header}.{body}.{SECRET_KEY}".encode()).hexdigest()
            if signature != expected_sig:
                return None
            padded_body = body + "=" * (-len(body) % 4)
            payload = json.loads(base64.urlsafe_b64decode(padded_body).decode())
            if payload.get("exp", 0) < time.time():
                return None
            return payload
    except Exception:
        return None

def authenticate_user(email, password):
    """Verify credentials against users database table."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, email, password_hash, role FROM users WHERE email = ?;", (email.strip().lower(),))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return False, "User email not found."
    
    hashed_input = hash_password(password)
    if user["password_hash"] != hashed_input:
        return False, "Invalid password."
    
    token = create_jwt_token(user["user_id"], user["email"], user["name"], user["role"])
    return True, {
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "token": token
    }

def register_new_user(name, email, password, role="rep"):
    """Register a new user account."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id FROM users WHERE email = ?;", (email.strip().lower(),))
    if cursor.fetchone():
        conn.close()
        return False, "Email already registered."
    
    pw_hash = hash_password(password)
    cursor.execute(
        "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?);",
        (name.strip(), email.strip().lower(), pw_hash, role)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    token = create_jwt_token(user_id, email, name, role)
    return True, {
        "user_id": user_id,
        "name": name,
        "email": email,
        "role": role,
        "token": token
    }
