#!/usr/bin/env python
from mpi4py import MPI

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

# DATOS SOBRE EL GRAFO
index = [2,5,8,9,10,11,12] # nº vecinos por nodo (acumulativo)
edges = [1,2,0,3,4,0,5,6,1,1,2,2] # nodos vecinos

# SOLO CON 7 PROCESOS
if (miRango == 0):
   CompruebaTopo("Comunicador original",com)

if numProcs != 7:
   if miRango == 0:
      print("ERROR: lanzar el programa con 7 procesos")
   quit()

# CREACIÓN COMUNICADOR GRAFO
comGraph = com.Create_graph(index, edges)

# PRINTS DE RANGO Y VECINOS
if (miRango == 0):
   CompruebaTopo("Comunicador nuevo",comGraph)

print("Soy el nodo %d y tengo %d vecinos:" % (miRango,comGraph.nneighbors), comGraph.neighbors)


### ------- CONSOLA ------- ###
### ------- CONSOLA ------- ###
# (mpi) $ mpirun -np 7 21-GraphTopo.py
#
# Comunicador original: topología sin definir
#
# Soy el nodo 1 y tengo 3 vecinos: [0, 3, 4]
# Soy el nodo 2 y tengo 3 vecinos: [0, 5, 6]
# Soy el nodo 3 y tengo 1 vecinos: [1]
# Soy el nodo 4 y tengo 1 vecinos: [1]
# Soy el nodo 5 y tengo 1 vecinos: [2]
# Soy el nodo 6 y tengo 1 vecinos: [2]
#
# Comunicador nuevo: topología en grafo
#
# Soy el nodo 0 y tengo 2 vecinos: [1, 2]
### ----------------------- ###




