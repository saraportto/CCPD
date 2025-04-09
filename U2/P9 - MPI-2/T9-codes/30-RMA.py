#! /usr/bin/env python
from mpi4py import MPI
import numpy as np

# INICIALIZACIÓN MPI
com = MPI.COMM_WORLD
numProcs = com.Get_size()
miRango = com.Get_rank()

# PRINT DE LO QUE SE VA A CALCULAR
if miRango==0:
    expo = 3
    cad = "Vamos a calcular: "
    for i in range(1,numProcs+1):
        cad = cad + "(%d^%d)" % (i,expo)
        if i!=numProcs:
            cad = cad +"+"
    print(cad)

# CREACIÓN VENTANA
if miRango==0: # solo el proceso 0 tiene memoria compartida
    expo_mem = np.array([expo]) # exponente
    result_mem = np.array([0]) # resultado
else:
    expo_mem = None
    result_mem = None

expo_win = MPI.Win.Create(expo_mem,comm=com) # ventana para el exponente
result_win = MPI.Win.Create(result_mem,comm=com) # ventana para el resultado

# CÁLCULO DEL EXPONENTE
expo_leido = np.array([0]) # exponente leído inicializado
expo_win.Fence() # SINCRONIZACIÓN
expo_win.Get(expo_leido, target_rank=0) # todos los procesos leen expo_win de 0 y lo guardan en expo_leido
expo_win.Fence() # SINCRONIZACIÓN

mi_numero = pow((miRango+1),expo_leido[0]) # cálculo cada número (proceso)
print("Proceso %d/%d: exponente=%d - número=%d" % (miRango, numProcs, expo_leido[0], mi_numero))

# CÁLCULO DEL RESULTADO
result_win.Fence() # SINCRONIZACIÓN
result_win.Accumulate(mi_numero, target_rank=0, op=MPI.SUM) # cada proceso SUMA mi_numero a result_win (del rango 0)
result_win.Fence() # SINCRONIZACIÓN

# IMPRIMIR RESULTADO
if miRango == 0:
    print("El resultado es:",result_mem[0])

# LIBERA VENTANAS
expo_win.Free()
result_win.Free()


### ------- CONSOLA --------- ###
# % mpirun -np 4 python 30-RMA.py 
# Vamos a calcular: (1^3)+(2^3)+(3^3)+(4^3)
# Proceso 0/4: exponente=3 - número=1
# Proceso 3/4: exponente=3 - número=64
# Proceso 1/4: exponente=3 - número=8
# Proceso 2/4: exponente=3 - número=27
# El resultado es: 100

### ------------------------- ###