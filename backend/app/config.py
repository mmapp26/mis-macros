from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    APP_NAME: str = "Mis Macros"
    ENV: str = os.getenv("ENV", "dev")
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    JWT_EXPIRE_MIN: int = 60 * 24 * 7  # 7 días
    USDA_API_KEY: str | None = None

    # Defaults UI / cálculo
    FIBER_MIN_G: int = 25
    PROTEIN_G_PER_KG: float = 2.0
    FAT_MIN_G_PER_KG: float = 0.8
    RECOMP_PCT: float = -0.12
    LOSS_PCT: float = -0.15
    GAIN_PCT: float = 0.10
    LOWCARB_DEFAULT_NET_CARBS: int = 50
    LOWCARB_DEFAULT_DAYS: List[int] = [0,1]  # Lunes(0), Martes(1)
    WATER_AI_WOMAN_ML: int = 2000
    WATER_AI_MAN_ML: int = 2500

    class Config:
        env_file = ".env"

settings = Settings()  # se inicializa con env vars