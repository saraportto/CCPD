#!/usr/bin/env python
from mpi4py import MPI
import numpy as np


## INICIALIZACIÓN MPI
com = MPI.COMM_WORLD
miRango = com.rank
numProcs = com.size


## SOLO CON Nº PROCESOS PARES
if numProcs%2 != 0:
    if miRango == 0:
        print("ERROR: lanzar el programa con un número par de procesos")
    quit()

## GENERA UN NÚMERO ALEATORIO
randNum =  np.random.randint(low=0, high=100, dtype=np.int32)

print("Proceso %d/%d: %d" % (miRango, numProcs, randNum))


## RANGOS IMPAR
rangosPar = [i for i in range(numProcs) if i%2 == 0]

# TODO: completar para crear comunicador comPar
gruposPar = com.group.Incl(rangosPar)
comPar = com.Create(gruposPar)


## RANGOS IMPAR
rangosImpar = [i for i in range(numProcs) if i%2 != 0]

# TODO: completar para crear comunicador comImpar
gruposImpar = com.group.Incl(rangosImpar)
comImpar = com.Create(gruposImpar)


## CREA VARIABLE SUMA
# TODO: modificar para crear variable suma en procesos 0 y 1

if miRango == (0 or 1): # procesos 0 y 1 crean variable suma con np array de ceros
    suma = np.zeros(1, dtype=np.int32)
    suma[0] = randNum

else:
    suma = np.zeros(1, dtype=np.int32)


## REDUCE
# TODO: usar Reduce en los comunicadores comPar y comImpar para calcular las sumas

if miRango in rangosPar: # si es rango par
    comPar.Reduce(randNum, suma, op=MPI.SUM, root=0)  # root del comunicador INTERNO (no del global)

else: # si es rango impar
    comImpar.Reduce(randNum, suma, op=MPI.SUM, root=0)  # root del comunicador INTERNO (no del global)


## IMPRIME RESULTADOS
if miRango == 0: # rango 0 --> suma procesos pares
    print("Suma de los pares: ", suma)

elif miRango == 1: # rango 1 --> suma procesos impares
    print("Suma de los impares: ", suma)