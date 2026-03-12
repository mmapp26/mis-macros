from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db, Base, engine
from .models import User, Profile, SexoEnum, ActividadEnum, ObjetivoEnum
from .schemas import UserCreate, Token, ProfileOut

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_password_hash(p: str) -> str:
    return pwd_context.hash(p)

def verify_password(p: str, hashed: str) -> bool:
    return pwd_context.verify(p, hashed)

def create_access_token(data: dict, expires_minutes: int = settings.JWT_EXPIRE_MIN):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # crea usuario + perfil
    exists = db.query(User).filter(User.email == user_in.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user = User(email=user_in.email, password_hash=get_password_hash(user_in.password),
                role="user", created_at=datetime.utcnow().isoformat())
    db.add(user); db.flush()
    agua_ml = (settings.WATER_AI_WOMAN_ML if user_in.sexo == SexoEnum.mujer else settings.WATER_AI_MAN_ML) if not user_in.agua_obj_ml else user_in.agua_obj_ml
    prof = Profile(
        user_id=user.id, nombre=user_in.nombre, sexo=user_in.sexo,
        altura_cm=user_in.altura_cm, fecha_nacimiento=user_in.fecha_nacimiento,
        peso_actual_kg=user_in.peso_actual_kg, actividad=user_in.actividad,
        objetivo=user_in.objetivo, agua_obj_ml=agua_ml,
        lowcarb_dias=settings.LOWCARB_DEFAULT_DAYS,
        net_carbs_target_lowcarb=settings.LOWCARB_DEFAULT_NET_CARBS,
        tema="light"
    )
    db.add(prof); db.commit()
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}