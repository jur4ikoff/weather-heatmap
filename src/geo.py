def validate_geo_coordinate(coordinate: float) -> bool:
    """Функция проверяет координаты на валидность"""
    if coordinate < -180 or coordinate > 180:
        return False

    return True
