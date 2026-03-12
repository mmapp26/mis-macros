from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..database import get_db
from ..deps import get_current_user
from ..models import User, DayLog, Entry, Food, FoodUnit, WaterLog, ComidaEnum, TipoDiaEnum
from ..utils.units import per_amount_from_100g

router = APIRouter(prefix="/logs", tags=["logs"])

def get_or_create_daylog(db: Session, user_id: int, fecha: str, tipo: TipoDiaEnum | None = None) -> DayLog:
    dl = db.query(DayLog).filter(and_(DayLog.user_id==user_id, DayLog.fecha==fecha)).first()
    if not dl:
        dl = DayLog(user_id=user_id, fecha=fecha, tipo_dia=tipo or TipoDiaEnum.regular)
        db.add(dl); db.commit(); db.refresh(dl)
    return dl

@router.post("/entry")
def add_entry(fecha: str, comida: ComidaEnum, food_id: int, cantidad: float, unidad: str,
              db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dl = get_or_create_daylog(db, user.id, fecha)
    food = db.query(Food).get(food_id)
    if not food: raise HTTPException(404, "Alimento no existe")
    gramos_por_unidad = None
    if unidad != "g":
        fu = db.query(FoodUnit).filter(FoodUnit.food_id==food_id, FoodUnit.nombre_unidad==unidad).first()
        if fu: gramos_por_unidad = fu.gramos_por_unidad
    # calcula macros “congelados”
    kcal = per_amount_from_100g(food.kcal_100g, food.base, food.porcion_base, cantidad, unidad, gramos_por_unidad)
    prot = per_amount_from_100g(food.prot_100g, food.base, food.porcion_base, cantidad, unidad, gramos_por_unidad)
    carb = per_amount_from_100g(food.carb_100g, food.base, food.porcion_base, cantidad, unidad, gramos_por_unidad)
    grasa = per_amount_from_100g(food.grasa_100g, food.base, food.porcion_base, cantidad, unidad, gramos_por_unidad)
    fibra = per_amount_from_100g(food.fibra_100g, food.base, food.porcion_base, cantidad, unidad, gramos_por_unidad)

    e = Entry(day_log_id=dl.id, comida=comida, food_id=food_id, cantidad=cantidad, unidad=unidad,
              kcal=kcal, prot=prot, grasa=grasa, carb=carb, fibra=fibra)
    db.add(e); db.commit()
    return {"ok": True, "entry_id": e.id}

@router.delete("/entry/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    e = db.query(Entry).get(entry_id)
    if not e: raise HTTPException(404, "No existe")
    # seguridad básica: que la entrada sea de un day_log del usuario
    dl = db.query(DayLog).get(e.day_log_id)
    if dl.user_id != user.id: raise HTTPException(403, "Sin permiso")
    db.delete(e); db.commit()
    return {"ok": True}

@router.post("/water")
def add_water(fecha: str, ml: int = 250, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dl = get_or_create_daylog(db, user.id, fecha)
    w = WaterLog(day_log_id=dl.id, ml=ml)
    db.add(w); db.commit()
    return {"ok": True}

@router.post("/copy")
def copy_entries(req_fecha_src: str, req_fecha_dst: str, scope: str, alimento_ids: list[int] | None = None,
                 db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # “Añadir” (no sustituir) – copiar entradas según scope
    src = get_or_create_daylog(db, user.id, req_fecha_src)
    dst = get_or_create_daylog(db, user.id, req_fecha_dst)
    q = db.query(Entry).filter(Entry.day_log_id==src.id)
    if scope in ("desayuno","comida","cena","snacks"):
        comidas = {
            "desayuno": ["Desayuno"],
            "comida": ["Comida"],
            "cena": ["Cena"],
            "snacks": ["Snack1","Snack2"]
        }[scope]
        q = q.filter(Entry.comida.in_(comidas))
    elif scope == "alimentos" and alimento_ids:
        q = q.filter(Entry.food_id.in_(alimento_ids))
    for e in q.all():
        db.add(Entry(day_log_id=dst.id, comida=e.comida, food_id=e.food_id,
                     cantidad=e.cantidad, unidad=e.unidad,
                     kcal=e.kcal, prot=e.prot, grasa=e.grasa, carb=e.carb, fibra=e.fibra))
    db.commit()
    return {"ok": True}