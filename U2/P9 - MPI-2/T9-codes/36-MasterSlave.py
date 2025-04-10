#! /usr/bin/env python
from mpi4py import MPI
import numpy as np
import sys

# NÚMERO DE HIJOS
nHijos = 8

# SI NO SE PASAN ARGUMENTOS --> envía datos a los hijos
if len(sys.argv)==1:

    # INICIALIZACIÓN MPI
    com = MPI.COMM_WORLD
    numProcs = com.Get_size()
    miRango = com.Get_rank()

    # SOLO CON UN PROCESO
    if numProcs != 1:
        if miRango == 0:
            print("ERROR: lanzar el programa con un proceso")
        quit()

    # MATRIZ Y VECTOR

    # vector: [1,2,3,4,5,6,7,8]
    vector=np.arange(start=1, stop=nHijos+1, dtype=int) 

    # matriz: cada fila es el vector, desplazado por i*nHijos
    matriz=np.tile(vector, (nHijos,1))
    for i in range(nHijos):
        matriz[i] = matriz[i] + i*nHijos
    print("Vector:\n",vector)
    print("Matriz:\n",matriz)
    
    # CREACIÓN HIJOS
    intercom = com.Spawn(sys.executable, args=[sys.argv[0], "hijo"], maxprocs=nHijos)
    # sys.executable: ejecuta el mismo programa
    # args: argumentos a pasar al hijo
    # maxprocs: número máximo de procesos a crear

    # ENVÍO MATRIZ Y VECTOR A HIJOS
    num = np.zeros(1, dtype=int)
    result_vector = np.zeros(nHijos, dtype=int)
    for i in range(nHijos):
        intercom.Send(matriz[i], dest=i)
        intercom.Send(vector, dest=i)
        intercom.Recv(num, source=i)
        result_vector[i]=num[0]
    print("Resultado:\n",result_vector)


# SI SE PASA ARGUMENTO "HIJO" --> recibe datos de los padres
elif sys.argv[1] == "hijo":

    intercom = MPI.Comm.Get_parent() # conecta con el padre
    miRangoHijo = intercom.Get_rank() # rango 
    fila = np.zeros(nHijos, dtype=int)
    intercom.Recv(fila, source=0)
    vector = np.zeros(nHijos, dtype=int)
    intercom.Recv(vector, source=0)
    result = np.dot(vector,fila)
    intercom.Send(result,dest=0)


### ------- CONSOLA --------- ###
# (mpi) $ mpirun -np 1 ./36-MasterSlave.py
# Vector:
#  [1 2 3 4 5 6 7 8]
# Matriz:
#  [[ 1  2  3  4  5  6  7  8]
#  [ 9 10 11 12 13 14 15 16]
#  [17 18 19 20 21 22 23 24]
#  [25 26 27 28 29 30 31 32]
#  [33 34 35 36 37 38 39 40]
#  [41 42 43 44 45 46 47 48]
#  [49 50 51 52 53 54 55 56]
#  [57 58 59 60 61 62 63 64]]
# Resultado:
#  [ 204  492  780 1068 1356 1644 1932 2220]

#### ------------------------- ###