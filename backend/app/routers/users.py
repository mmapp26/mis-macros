from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_current_user
from ..database import get_db
from ..models import User, Profile, Weight
from ..schemas import ProfileOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=ProfileOut)
def me(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Profile).get(user.id)

@router.post("/me/tema")
def set_theme(tema: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    prof = db.query(Profile).get(user.id)
    prof.tema = tema
    db.commit()
    return {"ok": True}

@router.post("/weights")
def add_weight(fecha: str, peso_kg: float, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    w = Weight(user_id=user.id, fecha=fecha, peso_kg=peso_kg)
    db.add(w); db.commit()
    # actualiza peso actual
    prof = db.query(Profile).get(user.id)
    prof.peso_actual_kg = peso_kg
    db.commit()
    return {"ok": True}