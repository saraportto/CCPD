#!/usr/bin/env python
from mpi4py import MPI
import numpy as np

# INICIALIZACIÓN MPI
com = MPI.COMM_WORLD
numProcs = com.size
miRango = com.rank

# SOLO con 9 procesos
if numProcs != 9:
   if miRango == 0:
      print("ERROR: lanzar el programa con 9 procesos")
   quit()

# CREA VALOR
miValor=np.array([miRango],dtype=float) # valor = rango (en array de numpy)

# CREA MATRIZ VIEJA
if miRango==0: # rango 0
   matrizOld = np.zeros(shape=(3,3)) # matriz 3x3 de ceros

else: # resto de procesos
   matrizOld = None # matriz vacía

# HACE GATHER en el proceso 0 del valor de cada proceso en la matriz vieja
com.Gather(miValor, matrizOld, root=0)

# PRINTEA MATRIZ VIEJA
if miRango==0:
   print("Valores viejos:")
   print(matrizOld)

# CREA SUBGRUPO CON SPLIT
comSub = com.Split(color = miRango/3) # split por rangos divisibles entre 3
comSub.Bcast(miValor,root=0) # BROADCAST de miValor (de rango 0 del subgrupo) a los demás procesos del subgrupo

# CREA MATRIZ NUEVA
if miRango==0: # rango 0
   matrizNew = np.zeros(shape=(3,3)) # matriz 3x3 de ceros

else: # resto de procesos
   matrizNew = None # matriz vacía

# HACE GATHER en el proceso 0 del valor de cada proceso en la matriz nueva
com.Gather(miValor, matrizNew, root=0)

# PRINTEA MATRIZ NUEVA
if miRango==0:
   print("Valores nuevos:")
   print(matrizNew)


###  ------- CONSOLA ------- ###
# (mpi) $ mpirun -np 9 ./14-IntracommsSplit.py
# Valores viejos:
# [[0. 1. 2.]
#  [3. 4. 5.]
#  [6. 7. 8.]]
#  
# Valores nuevos:
# [[0. 0. 0.]
#  [3. 3. 3.]
#  [6. 6. 6.]]

### ----------------------- ###