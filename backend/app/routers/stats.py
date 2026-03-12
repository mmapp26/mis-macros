from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..database import get_db
from ..deps import get_current_user
from ..models import DayLog, Entry, WaterLog, User
from ..schemas import StatsOut

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/week", response_model=StatsOut)
def week_stats(ending: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    end = datetime.fromisoformat(ending).date()
    start = end - timedelta(days=6)
    # agregados
    q = db.query(func.avg(Entry.kcal), func.avg(Entry.prot), func.avg(Entry.carb), func.avg(Entry.grasa), func.avg(Entry.fibra))\
          .join(DayLog, DayLog.id==Entry.day_log_id)\
          .filter(DayLog.user_id==user.id, DayLog.fecha>=start.isoformat(), DayLog.fecha<=end.isoformat())
    kcal, prot, carb, grasa, fibra = q.one()
    w = db.query(func.avg(WaterLog.ml)).join(DayLog, DayLog.id==WaterLog.day_log_id)\
          .filter(DayLog.user_id==user.id, DayLog.fecha>=start.isoformat(), DayLog.fecha<=end.isoformat()).scalar() or 0
    return StatsOut(
        semana=f"{start.isoformat()}_{end.isoformat()}",
        calorias_media=kcal or 0, prot_media=prot or 0, carb_media=carb or 0, grasa_media=grasa or 0,
        fibra_media=fibra or 0, agua_media_ml=w or 0, cumplimiento_calorias_pct=0.0
    )