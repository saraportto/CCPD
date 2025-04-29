# IMPORTS
from ej2_SumaRiemann_Cython import cython_riemann_sum, cython_riemann_sum_noloops
import numpy as np
from timeit import timeit

# GLOBALES
numbers = 10
TRUE_VALUE = 1.0  # Valor exacto de la integral
A = 0  # límite inferior
B = np.pi  # límite superior

# FUNCIÓN DE SUMA DE RIEMANN
def riemann_sum(n):
    dx = (B - A) / n # ancho de los intervalos
    riemann_sum = 0 # inicializa la suma de Riemann

    for i in range(n):
        x = A + i*dx  # Punto izquierdo del intervalo
        riemann_sum += np.sin(x) * dx # suma de Riemann

    return riemann_sum

# SUMA DE RIEMANN
print("\n", cython_riemann_sum(numbers))
print("\n", cython_riemann_sum_noloops(numbers))

# ASSERT
np.testing.assert_almost_equal(cython_riemann_sum(numbers), TRUE_VALUE)
np.testing.assert_almost_equal(cython_riemann_sum_noloops(numbers), TRUE_VALUE)

# TIMING
print("\nSuma de Riemann Cython, con bucles:")
print(timeit(lambda: cython_riemann_sum(numbers), number=1000))

print("\nSuma de Riemann Cython, sin bucles")
print(timeit(lambda: cython_riemann_sum_noloops(numbers), number=1000))