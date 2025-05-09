cimport numpy
import numpy as np

def cython_addvec(double [::1] vec, double value):
    """
    Añade un valor a cada elemento de un vector de NumPy.

    Args:
      vec: Un array unidimensional de NumPy de tipo double.
      value: El valor a añadir a cada elemento.

    Returns:
        Un nuevo array de NumPy con el mismo tipo y forma que vec,
        donde cada elemento ha sido incrementado por value.
    """

    # Tipos estáticos:
    # vec es un vector unidimensional C-contiguous
    # [1::] sería Fortran-contiguous
    # [: , ::1] sería bidimensional C-contiguous

  cdef: # Definición de variables con tipos estáticos
     int m = vec.shape[0]
     double[::1] result = np.zeros(m)

  for i in range(len(vec)):
    result[i] = vec[i] + value

  return result

