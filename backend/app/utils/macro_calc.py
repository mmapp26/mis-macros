from . import macro_calc
from ..models import SexoEnum, ActividadEnum, ObjetivoEnum
from ..config import settings

def actividad_factor(a: ActividadEnum) -> float:
    return {
        ActividadEnum.sedentaria: 1.2,
        ActividadEnum.ligera: 1.375,
        ActividadEnum.moderada: 1.55,
        ActividadEnum.alta: 1.725,
        ActividadEnum.muy_alta: 1.9,
    }[a]

def mifflin_st_jeor(sexo: SexoEnum, peso_kg: float, altura_cm: int, edad: int) -> float:
    # Hombre: 10*kg + 6.25*cm - 5*edad + 5; Mujer: ... - 161
    base = 10*peso_kg + 6.25*altura_cm - 5*edad
    return base + (5 if sexo == SexoEnum.hombre else -161)

def objetivo_pct(obj: ObjetivoEnum) -> float:
    return {
        ObjetivoEnum.perder: settings.LOSS_PCT,
        ObjetivoEnum.mantener: 0.0,
        ObjetivoEnum.ganar: settings.GAIN_PCT,
        ObjetivoEnum.recomposicion: settings.RECOMP_PCT,
    }[obj]

def calcular_macros(sexo: SexoEnum, peso_kg: float, altura_cm: int, edad: int, actividad: ActividadEnum,
                    objetivo: ObjetivoEnum, lowcarb: bool, net_carbs_target: int):
    bmr = mifflin_st_jeor(sexo, peso_kg, altura_cm, edad)
    tdee = bmr * actividad_factor(actividad)
    calorias = tdee * (1 + objetivo_pct(objetivo))

    prot_g = settings.PROTEIN_G_PER_KG * peso_kg
    if lowcarb:
        net_carb_g = net_carbs_target
        carb_total_g = net_carb_g + settings.FIBER_MIN_G
        kcal_restantes = calorias - (prot_g*4 + carb_total_g*4)
        grasa_g = max(kcal_restantes/9, 0)
        return calorias, prot_g, grasa_g, carb_total_g, settings.FIBER_MIN_G, net_carb_g
    else:
        grasa_min_g = settings.FAT_MIN_G_PER_KG * peso_kg
        kcal_restantes = calorias - (prot_g*4 + grasa_min_g*9)
        carb_g = max(kcal_restantes/4, 0)
        return calorias, prot_g, grasa_min_g, carb_g, settings.FIBER_MIN_G, carb_g - settings.FIBER_MIN_G