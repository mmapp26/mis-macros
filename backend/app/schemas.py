from pydantic import BaseModel, EmailStr
from typing import Optional, List
from .models import SexoEnum, ActividadEnum, ObjetivoEnum, ComidaEnum, TipoDiaEnum

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str
    sexo: SexoEnum
    altura_cm: int
    fecha_nacimiento: str
    peso_actual_kg: float
    actividad: ActividadEnum
    objetivo: ObjetivoEnum
    agua_obj_ml: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProfileOut(BaseModel):
    nombre: str
    sexo: SexoEnum
    altura_cm: int
    fecha_nacimiento: str
    peso_actual_kg: float
    actividad: ActividadEnum
    objetivo: ObjetivoEnum
    agua_obj_ml: int
    lowcarb_dias: List[int]
    net_carbs_target_lowcarb: int
    tema: str

    class Config:
        from_attributes = True

class FoodIn(BaseModel):
    nombre: str
    kcal: float
    proteinas: float
    grasas: float
    carbohidratos: float
    fibra: float
    unidad_base: str = "100g"  # "100g" | "unidad"
    porcion_base: float = 100.0

class FoodOut(BaseModel):
    id: int
    nombre: str
    kcal_100g: float
    prot_100g: float
    grasa_100g: float
    carb_100g: float
    fibra_100g: float
    is_system: bool

    class Config:
        from_attributes = True

class EntryIn(BaseModel):
    fecha: str
    comida: ComidaEnum
    food_id: int
    cantidad: float
    unidad: str  # g | unidad | taza | ...

class CopyRequest(BaseModel):
    desde_fecha: str
    hasta_fecha: str
    scope: str  # "dia"|"desayuno"|"comida"|"cena"|"snacks"|"alimentos" (lista ids)
    alimento_ids: Optional[List[int]] = None

class StatsOut(BaseModel):
    semana: str
    calorias_media: float
    prot_media: float
    carb_media: float
    grasa_media: float
    fibra_media: float
    agua_media_ml: float
    cumplimiento_calorias_pct: float