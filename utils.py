# utils.py
def calculate_movement(prev, current):
    """İki zaman dilimindeki pozisyon farkını hesapla"""
    return abs(current - prev) > 0.02  # Belirli bir eşik değeri belirlenebilir
