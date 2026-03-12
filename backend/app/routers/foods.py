from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import get_db
from ..deps import get_current_user
from ..models import Food, FoodUnit, Favorite, User
from ..schemas import FoodIn, FoodOut

router = APIRouter(prefix="/foods", tags=["foods"])

@router.get("/search", response_model=list[FoodOut])
def search(q: str = Query(min_length=1), limit: int = 15, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    items = db.query(Food).filter(Food.nombre.ilike(f"%{q}%")).order_by(Food.is_system.desc()).limit(limit).all()
    return items

@router.post("", response_model=FoodOut)
def create(food: FoodIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    f = Food(
        nombre=food.nombre.strip(),
        kcal_100g=food.kcal, prot_100g=food.proteinas, grasa_100g=food.grasas,
        carb_100g=food.carbohidratos, fibra_100g=food.fibra,
        base=food.unidad_base, porcion_base=food.porcion_base,
        autor_user_id=user.id, is_system=False, fuente="USER"
    )
    db.add(f); db.commit(); db.refresh(f)
    return f

@router.delete("/{food_id}")
def delete(food_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    f = db.query(Food).get(food_id)
    if not f: raise HTTPException(404, "No existe")
    if f.is_system: raise HTTPException(400, "No se puede borrar alimentos del sistema")
    if not (user.role == "admin" or f.autor_user_id == user.id):
        raise HTTPException(403, "Sin permiso")
    db.delete(f); db.commit()
    return {"ok": True}

@router.post("/{food_id}/favorite")
def favorite(food_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db.merge(Favorite(user_id=user.id, food_id=food_id)); db.commit()
    return {"ok": True}