#!/usr/bin/env python

from mpi4py import MPI
import numpy as np

# INICIALIZACIÓN MPI
com = MPI.COMM_WORLD
numProcs = com.size
miRango = com.rank
miRango_vec = np.array([com.rank])

# SOLO con 8 procesos
if numProcs != 8:
    if miRango == 0:
        print("ERROR: lanzar el programa con 8 procesos")
    quit()

# GRUPO con 
grupo = miRango/4 # a qué grupo pertenece el proceso (el 0 o el 1)
comSub = com.Split(color = grupo) # crear subgrupo con el color del grupo

# MARCAR LÍDER LOCAL Y REMOTO

# Del grupo 0 (0, 1, 2, 3)
if grupo == 0:
    local_leader = 0
    remote_leader = 4

# Del grupo 1 (4, 5, 6, 7)
else:
    local_leader = 0
    remote_leader = 0


# CREAR INTERCOMUNICADOR
comInt = MPI.Intracomm.Create_intercomm(comSub, local_leader, com, remote_leader)

# Rango en el intercomunicador
miRangoInt = comInt.rank

print("Rango %d  -  RangoInt %d  -  Grupo %d" %(miRango, miRangoInt, grupo))

# PROCESOS GRUPO 0 envían su rango al proceso del mismo rango del grupo 1 
if miRango <= 3:
    print("Hola, soy %d (%d) y envío mi rango a mi colega de la derecha" % (miRangoInt, miRango))
    comInt.Send(miRango_vec, dest = miRango)

# PROCESOS GRUPO 1 reciben el rango del proceso del mismo rango del grupo 0
if miRango >= 4:
    valor = np.zeros(1)
    comInt.Recv(valor)
    print("Hola, soy %d (%d) y recibo un: %d de mi colega de la izqda." %(miRangoInt, miRango, valor[0]))


###  ------- CONSOLA ------- ###
# (mpi) $ mpirun -np 8 ./15-Intercomms.py

# Rango 0  -  RangoInt 0  -  Grupo 0
# Rango 1  -  RangoInt 1  -  Grupo 0
# Rango 2  -  RangoInt 2  -  Grupo 0
# Rango 3  -  RangoInt 3  -  Grupo 0
# Rango 4  -  RangoInt 0  -  Grupo 1
# Rango 5  -  RangoInt 1  -  Grupo 1
# Rango 6  -  RangoInt 2  -  Grupo 1
# Rango 7  -  RangoInt 3  -  Grupo 1

# Hola, soy 2 (2) y envío mi rango a mi colega de la derecha
# Hola, soy 3 (3) y envío mi rango a mi colega de la derecha
# Hola, soy 2 (6) y recibo un: 2 de mi colega de la izquierda
# Hola, soy 3 (7) y recibo un: 3 de mi colega de la izquierda
# Hola, soy 0 (0) y envío mi rango a mi colega de la derecha
# Hola, soy 0 (4) y recibo un: 0 de mi colega de la izquierda
# Hola, soy 1 (1) y envío mi rango a mi colega de la derecha
# Hola, soy 1 (5) y recibo un: 1 de mi colega de la izquierda

### ----------------------- ###



