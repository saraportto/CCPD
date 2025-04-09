#! /usr/bin/env python

import numpy
from mpi4py import MPI

# INICIALIZACIÓN MPI
comm = MPI.COMM_WORLD
numProcs = comm.Get_size()
miRango = comm.Get_rank()

# SOLO CON 2 PROCESOS
if numProcs!=2:
    if miRango==0:
        print("ERROR: el programa debe ser ejecutado con 2 procesos")
    quit()

# CREACIÓN VENTANA
# proceso 1
if miRango == 1:
    a = numpy.zeros(9, dtype=numpy.int16) # inicializa array ceros 9 etos
    print("Proceso",miRango,"comparto", a)
    window = MPI.Win.Create(a, comm=comm) # crea ventana con a


# proceso 0
elif miRango == 0:
    window = MPI.Win.Create(None, comm=comm) # crea ventana sin datos

# ESCRITURA DE DATOS
# proceso 1
if miRango == 1:
    g1 = comm.group.Incl([0]) # crea grupo con proceso 0
    window.Post(group=g1) # PUBLICA ventana (comparte la ventana al grupo 1: proceso 0)
    window.Wait() # ESPERA a que el proceso 0 complete la ventana

# proceso 0
elif miRango == 0:
    g2 = comm.group.Incl([1]) # crea grupo con proceso 1
    b = numpy.full(9, 1, dtype=numpy.int16) # inicializa array 9 etos con 1s
    print("Proceso",miRango,"escribo", b) 
    window.Start(group=g2) # INICIA ventana (accede a la ventana del grupo 2: proceso 1)
    window.Put(b, target_rank=1) # ESCRIBE ventana del proceso 1 (a) con b
    window.Complete() # COMPLETA ventana

# PRINT
if miRango == 1:
    print("Proceso",miRango,"resultado", a)


### ------- CONSOLA --------- ###
# % mpirun -np 2 python 30-RMA-Post.py
# Proceso 1 comparto [0 0 0 0 0 0 0 0 0]
# Proceso 0 escribo [1 1 1 1 1 1 1 1 1]
# Proceso 1 resultado [1 1 1 1 1 1 1 1 1]
### ------------------------- ###


