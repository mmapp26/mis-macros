def per_amount_from_100g(value_per_100g: float, base: str, porcion_base: float, cantidad: float, unidad: str, gramos_por_unidad: float | None = None) -> float:
    """
    Devuelve el valor nutricional para la cantidad/unidad seleccionada.
    - Si base="100g" -> regla de tres por gramos.
    - Si base="unidad" -> usamos porcion_base (normalmente 1 unidad) o conversion a gramos si se introdujo.
    """
    if base == "100g":
        if unidad == "g":
            return value_per_100g * (cantidad / 100.0)
        elif unidad in ("unidad","taza","cucharada"):
            if gramos_por_unidad is None:
                raise ValueError("Falta gramaje por unidad")
            return value_per_100g * (gramos_por_unidad / 100.0) * cantidad
        else:
            raise ValueError("Unidad no soportada")
    else:  # base=unidad
        # value_per_100g en este caso será “por unidad” si porcion_base=1
        factor = cantidad / porcion_base
        return value_per_100g * factor