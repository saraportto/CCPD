#!/usr/bin/env python
from mpi4py import MPI

# TAMAÑO DIMENSIONES MALLA
SIZE_X = 4
SIZE_Y = 3

# COMPROBACIÓN TOPOLOGÍA
def CompruebaTopo(cad,communic):
   topo = communic.Get_topology()
   if topo == MPI.CART:
      print("%s: topología cartesiana" % cad)
   elif topo == MPI.GRAPH:
      print("%s: topología en grafo" % cad)
   elif topo == MPI.UNDEFINED:
      print("%s: topología sin definir" % cad)

# INICIALIZACIÓN MPI
com = MPI.COMM_WORLD
numProcs = com.size
miRango = com.rank

# SOLO CON 12 PROCESOS
if (miRango == 0):
   CompruebaTopo("Comunicador original",com)

if numProcs != 12:
   if miRango == 0:
      print("ERROR: lanzar el programa con 12 procesos")
   quit()

# CREACIÓN COMUNICADOR CARTESIANO
comCartesiano = com.Create_cart((SIZE_X,SIZE_Y),(1,0))
# com: comunicador original
# SIZE_X, SIZE_Y: dimensiones de la malla
# (1,0): periodicidad en la dirección 0, no en la 1

# COMPROBACIÓN TOPOLOGÍA
if (miRango == 0):
   CompruebaTopo("Comunicador nuevo",comCartesiano)

# RANGO EN EL NUEVO COMUNICADOR: Get_cart_rank
if miRango==0:
   for i in range(SIZE_X):
      for j in range(SIZE_Y):
         r = comCartesiano.Get_cart_rank([i,j])
         print("El proceso de coordenadas (%d,%d) tiene rango %d" %(i,j,r))

# DEMO Shift(direcc, dist)
if (miRango == 0):
   data1,data2 = comCartesiano.Shift(0,1)
   print("Dirección 0, distancia 1, nodo1 %d, nodo2 %d" % (data1,data2))
   data1,data2 = comCartesiano.Shift(1,1)
   print("Dirección 1, distancia 1, nodo1 %d, nodo2 %d" % (data1,data2))
   data1,data2 = comCartesiano.Shift(0,5)
   print("Dirección 0, distancia 5, nodo1 %d, nodo2 %d" % (data1,data2))
   data1,data2 = comCartesiano.Shift(1,5)
   print("Dirección 1, distancia 5, nodo1 %d, nodo2 %d" % (data1,data2))


### ------- CONSOLA ------- ###
# (mpi) $ mpirun -np 12 ./20-CartTopo.py
#
# Comunicador original: topología sin definir
# Comunicador nuevo: topología cartesiana
#
# El proceso de coordenadas (0,0) tiene rango 0
# El proceso de coordenadas (0,1) tiene rango 1
# El proceso de coordenadas (0,2) tiene rango 2
# El proceso de coordenadas (1,0) tiene rango 3
# El proceso de coordenadas (1,1) tiene rango 4
# El proceso de coordenadas (1,2) tiene rango 5
# El proceso de coordenadas (2,0) tiene rango 6
# El proceso de coordenadas (2,1) tiene rango 7
# El proceso de coordenadas (2,2) tiene rango 8
# El proceso de coordenadas (3,0) tiene rango 9
# El proceso de coordenadas (3,1) tiene rango 10
# El proceso de coordenadas (3,2) tiene rango 11
#
# Dirección 0, distancia 1, nodo1 9, nodo2 3
# Dirección 1, distancia 1, nodo1 -2, nodo2 1
# Dirección 0, distancia 5, nodo1 9, nodo2 3
# Dirección 1, distancia 5, nodo1 -2, nodo2 -2

### ----------------------- ###




