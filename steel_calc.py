import math

def calculate_three_panel_inertia(width_mm, area_single_cm2, inertia_single_cm4, inertia_per_meter_cm4):
    B = width_mm
    E = area_single_cm2
    G = inertia_single_cm4
    K = inertia_per_meter_cm4
    if None in (B, E, G, K) or E <= 0:
        return None
    temp = (K * (2 * B / 1000) - 2 * G) / (E * 2)
    if temp <= 0:
        return None
    x = math.sqrt(temp) * 10
    term1 = x * E / (E * 3)
    part1 = (term1 + x) ** 2 * E
    part2 = (x - term1) ** 2 * 2 * E
    I_three = (part1 + part2) / 100 + 3 * G
    return I_three

def calculate_three_panel_modulus(I_three_cm4, height_mm, area_single_cm2, inertia_single_cm4, inertia_per_meter_cm4, width_mm):
    if I_three_cm4 is None:
        return None
    C = height_mm
    E = area_single_cm2
    G = inertia_single_cm4
    K = inertia_per_meter_cm4
    B = width_mm
    if None in (C, E, G, K, B):
        return None
    temp = (K * (2 * B / 1000) - 2 * G) / (E * 2)
    if temp <= 0:
        return None
    x = math.sqrt(temp) * 10
    term1 = x * E / (E * 3)
    denominator = (term1 + C) / 10
    if denominator <= 0:
        return None
    return I_three_cm4 / denominator

def calculate_double_pile_inertia(inertia_single_cm4, modulus_single_cm3, area_single_cm2):
    G = inertia_single_cm4
    H = modulus_single_cm3
    E = area_single_cm2
    if None in (G, H, E) or H <= 0:
        return None
    d = (G / H) * 10
    I_double = ((d ** 2) * E * 2) / 100 + G * 2
    return I_double

def calculate_double_pile_modulus(I_double_cm4, inertia_single_cm4, modulus_single_cm3, height_mm, width_mm, area_single_cm2, inertia_per_meter_cm4):
    if I_double_cm4 is None:
        return None
    G = inertia_single_cm4
    H = modulus_single_cm3
    C = height_mm
    B = width_mm
    E = area_single_cm2
    K = inertia_per_meter_cm4
    if None in (G, H, C, B, E, K) or H <= 0 or E <= 0:
        return None
    term1 = (G / H) * 10
    temp = (K * (2 * B / 1000) - 2 * G) / (E * 2)
    if temp <= 0:
        return None
    sqrt_val = math.sqrt(temp) * 10
    denominator = term1 - sqrt_val + C
    if denominator <= 0:
        return None
    return (I_double_cm4 / denominator) * 10

def compute_all(params):
    I3 = calculate_three_panel_inertia(
        params['width_mm'], params['area_single_cm2'],
        params['inertia_single_cm4'], params['inertia_per_meter_cm4']
    )
    W3 = None
    if I3 is not None:
        W3 = calculate_three_panel_modulus(
            I3, params['height_mm'], params['area_single_cm2'],
            params['inertia_single_cm4'], params['inertia_per_meter_cm4'],
            params['width_mm']
        )
    I2 = calculate_double_pile_inertia(
        params['inertia_single_cm4'], params['modulus_single_cm3'],
        params['area_single_cm2']
    )
    W2 = None
    if I2 is not None:
        W2 = calculate_double_pile_modulus(
            I2, params['inertia_single_cm4'], params['modulus_single_cm3'],
            params['height_mm'], params['width_mm'], params['area_single_cm2'],
            params['inertia_per_meter_cm4']
        )
    return {
        "I_three_cm4": I3,
        "W_three_cm3": W3,
        "I_double_cm4": I2,
        "W_double_cm3": W2
    }