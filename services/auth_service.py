# services/auth_service.py
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from models.user_model import User, UserIn
from repositories.user_repository import user_repository_instance

# Configuration for JWT
SECRET_KEY = "YOUR_SECRET_KEY"  # Replace with an environment variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(email: str, password: str):
    user = user_repository_instance.get_user_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def register_user(user_in: UserIn) -> User:
    if user_repository_instance.get_user_by_email(user_in.email):
        raise Exception("User already exists")
    hashed_password = get_password_hash(user_in.password)
    return user_repository_instance.create_user(user_in.email, hashed_password)
