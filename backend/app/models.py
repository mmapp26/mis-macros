
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Float, Date, Enum, JSON, UniqueConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base
import enum

class SexoEnum(str, enum.Enum):
    mujer = "Mujer"
    hombre = "Hombre"

class ActividadEnum(str, enum.Enum):
    sedentaria="sedentaria"
    ligera="ligera"
    moderada="moderada"
    alta="alta"
    muy_alta="muy_alta"

class ObjetivoEnum(str, enum.Enum):
    perder="perder"
    mantener="mantener"
    ganar="ganar"
    recomposicion="recomposicion"

class TipoDiaEnum(str, enum.Enum):
    regular="regular"
    lowcarb="lowcarb"

class ComidaEnum(str, enum.Enum):
    desayuno="Desayuno"
    snack1="Snack1"
    comida="Comida"
    snack2="Snack2"
    cena="Cena"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="user")
    created_at: Mapped[str] = mapped_column(String(30))

    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete")

class Profile(Base):
    __tablename__ = "profiles"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120))
    sexo: Mapped[SexoEnum] = mapped_column(Enum(SexoEnum))
    altura_cm: Mapped[int] = mapped_column(Integer)
    fecha_nacimiento: Mapped[str] = mapped_column(String(10))  # YYYY-MM-DD
    peso_actual_kg: Mapped[float] = mapped_column(Float)
    actividad: Mapped[ActividadEnum] = mapped_column(Enum(ActividadEnum))
    objetivo: Mapped[ObjetivoEnum] = mapped_column(Enum(ObjetivoEnum))
    agua_obj_ml: Mapped[int] = mapped_column(Integer)
    lowcarb_dias: Mapped[JSON] = mapped_column(JSON, default=[])
    net_carbs_target_lowcarb: Mapped[int] = mapped_column(Integer, default=50)
    tema: Mapped[str] = mapped_column(String(10), default="light")

    user = relationship("User", back_populates="profile")

class Weight(Base):
    __tablename__ = "weights"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    fecha: Mapped[str] = mapped_column(String(10))
    peso_kg: Mapped[float] = mapped_column(Float)

class Food(Base):
    __tablename__ = "foods"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), index=True)
    kcal_100g: Mapped[float] = mapped_column(Float)
    prot_100g: Mapped[float] = mapped_column(Float)
    grasa_100g: Mapped[float] = mapped_column(Float)
    carb_100g: Mapped[float] = mapped_column(Float)
    fibra_100g: Mapped[float] = mapped_column(Float)
    base: Mapped[str] = mapped_column(String(20), default="100g")  # "100g" | "unidad"
    porcion_base: Mapped[float] = mapped_column(Float, default=100.0)  # 100g o 1 unidad
    autor_user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    fuente: Mapped[str] = mapped_column(String(10), default="USER") # "BEDCA"|"USDA"|"USER"
    extra: Mapped[JSON | None] = mapped_column(JSON, nullable=True)

class FoodUnit(Base):
    __tablename__ = "food_units"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"))
    nombre_unidad: Mapped[str] = mapped_column(String(40))  # taza, cucharada, unidad...
    gramos_por_unidad: Mapped[float] = mapped_column(Float)

    __table_args__ = (UniqueConstraint("food_id", "nombre_unidad", name="uq_food_unit"),)

class DayLog(Base):
    __tablename__ = "day_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    fecha: Mapped[str] = mapped_column(String(10), index=True)  # YYYY-MM-DD
    tipo_dia: Mapped[TipoDiaEnum] = mapped_column(Enum(TipoDiaEnum), default=TipoDiaEnum.regular)

class Entry(Base):
    __tablename__ = "entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day_log_id: Mapped[int] = mapped_column(ForeignKey("day_logs.id"), index=True)
    comida: Mapped[ComidaEnum] = mapped_column(Enum(ComidaEnum))
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"))
    cantidad: Mapped[float] = mapped_column(Float)   # cantidad en g/unid/taza
    unidad: Mapped[str] = mapped_column(String(20))  # g | unidad | taza | cucharada...
    # macros "congelados" al momento de registrar (evita cambios futuros)
    kcal: Mapped[float] = mapped_column(Float)
    prot: Mapped[float] = mapped_column(Float)
    grasa: Mapped[float] = mapped_column(Float)
    carb: Mapped[float] = mapped_column(Float)
    fibra: Mapped[float] = mapped_column(Float)

class WaterLog(Base):
    __tablename__ = "water_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day_log_id: Mapped[int] = mapped_column(ForeignKey("day_logs.id"), index=True)
    ml: Mapped[int] = mapped_column(Integer)

class Favorite(Base):
    __tablename__ = "favorites"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"), primary_key=True)