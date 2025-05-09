import numpy as np

num_elem = 10000

# PARTE PYTHON
# ---------------------------
def python_addvec(vec, value):
  result = np.empty_like(vec)
  for i in range(len(vec)):
    result[i] = vec[i] + value
  return result

a=np.arange(num_elem, dtype=np.double)
x = 4.5
b_python = python_addvec(a, x)


# PARTE CYTHON
# ---------------------------
from cython_addvec import cython_addvec # importa módulo del .pyx
b_cython = cython_addvec(a, x)


# COMPARACIÓN
# ---------------------------
np.testing.assert_array_equal(b_python, b_cython) #
print("Cython and Python results are equal.")


