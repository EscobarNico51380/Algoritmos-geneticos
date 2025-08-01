import numpy as np

def objective_function(L1, L2, L3, v, mi, mpj, c_d, rho, Ad, F_M):
    """
    Calcula la energía consumida por un UAV durante una entrega.
    Parámetros:
    - L1, L2, L3: distancias (en metros)
    - v: velocidad (m/s)
    - mi: masa del dron
    - mpj: masa del paquete
    - c_d, rho, Ad, F_M: constantes físicas
    """
    term1 = c_d * rho * Ad * (L1 + L2 + L3) * v**2
    term2 = L2 * np.sqrt(((mi + mpj) * 9.81)**3) / (v * F_M * np.sqrt(2 * rho * Ad))
    term3 = (L1 + L3) * np.sqrt((mi * 9.81)**3) / (v * F_M * np.sqrt(2 * rho * Ad))
    eta = 1  # eficiencia global (ajustable si la querés modelar)
    return (1/eta) * (term1 + term2 + term3)
