from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi_jwt_auth import AuthJWT
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, TokenResponse

SECRET_KEY = "your_secret_key"  # 🔹 Зміни на свій ключ!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@AuthJWT.load_config
def get_config():
    return {"authjwt_secret_key": SECRET_KEY}

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(identity: str, expires_delta: timedelta):
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": identity, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@auth_router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")

    new_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@auth_router.post("/login", response_model=TokenResponse)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(db_user.email, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_access_token(db_user.email, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

auth_router = APIRouter()

@auth_router.get("/verify")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Невірний токен")
    user.is_verified = True
    db.commit()
    return {"message": "Email успішно підтверджено!"}