#!/usr/bin/env python
from mpi4py import MPI
import numpy as np

com = MPI.COMM_WORLD
miRango = com.rank
numProcs = com.size

if numProcs%2 != 0:
    if miRango == 0:
        print("ERROR: lanzar el programa con un número par de procesos")
    quit()

randNum =  np.random.randint(low=0, high=100, dtype=np.int32)

print("Proceso %d/%d: %d" % (miRango, numProcs, randNum))

rangosPar = [i for i in range(numProcs) if i%2 == 0]
grupoPar = com.Get_group()
grupoPar = grupoPar.Incl(rangosPar)
comPar = com.Create(grupoPar)

rangosImpar = [i for i in range(numProcs) if i%2 != 0]
grupoImpar = com.Get_group()
grupoImpar = grupoImpar.Incl(rangosImpar)
comImpar = com.Create(grupoImpar)

if miRango <= 1 :
    suma = np.zeros(1, dtype=np.int32)
else:
    suma = None

if miRango in rangosPar:
    comPar.Reduce(randNum, suma, op=MPI.SUM, root=0)
else:
    comImpar.Reduce(randNum, suma, op=MPI.SUM, root=0)

if miRango == 0:
    print("Suma de los pares: ", suma)
elif miRango == 1:
    print("Suma de los impares: ", suma)