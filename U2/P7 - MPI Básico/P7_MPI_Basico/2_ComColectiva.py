#!/usr/bin/env python
"""
Partiendo del código ComColectiva_TODO.py, implementar en paralelo la suma de las columnas
de una matriz A (L filas, L*NP columnas, con NP procesos)
"""
from mpi4py import MPI
import numpy as np

L = 3 # tamaño bloque L*L
    
comm = MPI.COMM_WORLD
miRango = comm.rank
numProc = comm.size

if miRango == 0:
    A = np.random.randint(low=0, high=10, size=(L, L*numProc), dtype=np.int32)
    print("Matriz A:")
    print(A)
    A_t = np.empty(0, dtype=np.int32)
    for i in range(numProc):
        # A_t = np.concatenate([A_t, A[  ...TODO... ].ravel()])
        A_t = np.concatenate([A_t, A[ 0 : L, i*L : (i+1)*L].ravel()])
        # El método .ravel() convierte una submatriz de A en un vector unidimensional
        # y np.concatenate agrega ese vector a A_t, acumulando en A_t las columnas que
        # serán dispersadas a los procesos en paralelo.

        # El método .ravel() convierte una matriz en un vector
else:
    A_t = None

bloque=np.empty(shape=(L,L), dtype=np.int32)
# comm.Scatter(  ...TODO... )
comm.Scatter(A_t, bloque, root=0) # send_buf = A_t, recv_buf, root (nodo que hace el scatter)
bloque_sum = np.sum(bloque, axis=1, dtype=np.int32)

if miRango == 0:
    col = np.zeros(shape=(L,1), dtype=np.int32)
else:
    col = None

# comm.Reduce( ... TODO ...)
comm.Reduce(bloque_sum, col, op=MPI.SUM, root=0)
if miRango == 0:
    print("Resultado: ")
    print(col)