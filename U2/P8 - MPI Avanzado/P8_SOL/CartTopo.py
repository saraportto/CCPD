#!/usr/bin/env python
from mpi4py import MPI
import numpy as np

NFilas = 4
NCols = 4
comm = MPI.COMM_WORLD
numProcs = comm.size
miRango = comm.rank

if numProcs != (NFilas*NCols):
    if miRango == 0:
        print("** ERROR: lanzar el programa con %d procesos **" % (NFilas*NCols))
    quit()

commCartesiano = comm.Create_cart((NFilas,NCols),(0,0))

if commCartesiano.Get_topology() != MPI.CART:
    if miRango==0:
        print("** Error creando topología cartesiana **")
    quit()

miNum = np.random.randint(low=0, high=10, size=1, dtype=np.int32)

def mostrarDatos() :
    if miRango == 0:
        matriz = np.empty((NFilas, NCols), dtype = np.int32)
    else:
        matriz = None
    comm.Gather(miNum, matriz, root=0)
    if miRango == 0:
        print(matriz)

if miRango==0:
    print("Datos iniciales:")
mostrarDatos()

col1=np.empty(1)
fil1=np.empty(1)
col2=np.empty(1)
fil2=np.empty(1)
if miRango==0:
    fil1[0] = int(input("Fila elemento 1: "))
    col1[0] = int(input("Columna elemento 1: "))
    fil2[0] = int(input("Fila elemento 2: "))
    col2[0] = int(input("Columna elemento 2: "))
comm.Bcast(fil1, root=0)
comm.Bcast(col1, root=0)
comm.Bcast(fil2, root=0)
comm.Bcast(col2, root=0)

proc1 =commCartesiano.Get_cart_rank([fil1[0],col1[0]])
proc2 =commCartesiano.Get_cart_rank([fil2[0],col2[0]])

if miRango == 0:
    print("Intercambiando datos entre procesos con rangos %d, %d" % (proc1, proc2))

if miRango == proc1:
    aux = np.zeros(1, dtype=np.int32)
    comm.Send(miNum, dest=proc2)
    comm.Recv(aux)

if miRango == proc2:
    aux = np.zeros(1, dtype=np.int32)
    comm.Send(miNum, dest=proc1)
    comm.Recv(aux)

if miRango == proc1 or miRango == proc2:
    miNum = aux

if miRango == 0:
    print("Tras el intercambio: ")
    mostrarDatos()