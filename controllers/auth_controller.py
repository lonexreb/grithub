# controllers/auth_controller.py
from fastapi import APIRouter, HTTPException, status
from models.user_model import UserIn, UserOut
from services.auth_service import register_user, authenticate_user, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut)
async def register(user_in: UserIn):
    try:
        user = register_user(user_in)
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login")
async def login(user_in: UserIn):
    user = authenticate_user(user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
