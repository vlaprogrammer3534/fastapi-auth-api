from fastapi import FastAPI, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import timedelta, datetime
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

# DB setup and model import
from models import User, create_db, SessionLocal



# Step 1: Create tables
create_db()
print("✅ Tables created successfully.")

# Step 2: Initialize FastAPI app
app = FastAPI()

# Step 3: Dummy client credentials (temporary test keys)
FAKE_CLIENT_KEY = "myclient123"
FAKE_SECRET_KEY = "mysecret456"

# Step 4: JWT configuration
JWT_SECRET = "supersecurejwtsecret"          # Secret key for encoding JWT
JWT_ALGORITHM = "HS256"                      # Algorithm for encoding
JWT_EXPIRY_MINUTES = 15                      # Access token expiry
JWT_REFRESH_EXPIRY_DAYS = 7                  # Refresh token expiry

# Step 5: OAuth2 scheme for extracting token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Step 6: Pydantic model for login body
class LoginRequest(BaseModel):
    client_key: str
    secret_key: str

# Step 7: Create Access Token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT_EXPIRY_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

# Step 8: Create Refresh Token
def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=JWT_REFRESH_EXPIRY_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

# Step 9: Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Step 10: Login route to authenticate and generate tokens
@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Validate credentials
    if request.client_key != FAKE_CLIENT_KEY or request.secret_key != FAKE_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API keys")

    # If user exists, fetch it; else create new user
    user = db.query(User).filter(User.client_key == request.client_key).first()
    if not user:
        user = User(client_key=request.client_key, secret_key=request.secret_key)
        db.add(user)
        db.commit()
        db.refresh(user)

    # Generate tokens
    token_data = {"sub": request.client_key}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.id
    }

# ✅ Step 11: Extract current user from token (token validation)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        client_key = payload.get("sub")
        if not client_key:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.client_key == client_key).first()
    if not user:
        raise credentials_exception
    return user

# ✅ Step 12: Protected route to test access token
@app.get("/secure-data")
def get_secure_data(current_user: User = Depends(get_current_user)):
    return {
        "message": f"Welcome {current_user.client_key}, you have accessed secure data successfully!"
    }

# ✅ Step 13: Get current user info (like /me)
@app.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "client_key": current_user.client_key,
        "created_at": current_user.created_at
    }

# ✅ Step 14: Refresh token to get new access token
@app.post("/refresh-token")
def refresh_access_token(refresh_token: str = Body(...), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid refresh token")
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        client_key = payload.get("sub")
        if not client_key:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.client_key == client_key).first()
    if not user:
        raise credentials_exception

    # Generate new access token
    new_access_token = create_access_token(data={"sub": client_key})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@app.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    # For JWT stateless system, logout is handled on client by deleting token
    return {
        "message": f"User {current_user.client_key} logged out successfully.",
        "tip": "Please delete the token on client-side to complete logout."
    }
 