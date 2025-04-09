#!/usr/bin/env python
from mpi4py import MPI
import numpy as np
import time

sizeRand = 500000 # tamaño del array a enviar

# INICIALIZACIÓN MPI
comm = MPI.COMM_WORLD
my_rank = comm.rank
num_processes = comm.siz

# SE REALIZA CON DOS PROCESOS
if num_processes!=2:
   if my_rank == 0:
      print("*** ERROR: lanzar con dos procesos ***") # error si no se lanzan dos procesos

else:

   # ENVÍO DE DATOS (proceso 0)
   if my_rank == 0:
      randNum = np.random.random_sample(sizeRand) # array de envío
      print("Tarea 0: esperando comienzo de envío", flush=True)
      request = comm.Isend(randNum,dest=1) # envío de randNum al proceso 1
      print("Tarea 0: envío comenzado (%.3f, %.3f)" % (randNum[0], randNum[1]), flush=True)
      request.Wait() # espera a que el envío se complete
      print("Tarea 0: envío finalizado", flush=True)

   # RECEPCIÓN DE DATOS (proceso 1)
   elif my_rank == 1:
      time.sleep(1) # espera 1 segundo para asegurar que el envío se ha iniciado
      randNum2 = np.zeros(sizeRand) # buffer vacío
      print("Tarea 1: esperando comienzo de recepción", flush=True)
      request = comm.Irecv(randNum2, source=0) # recepción del envío del proceso 0 en randNum2
      print("Tarea 1: recepción comenzada", flush=True)
      request.Wait() # espera a que la recepción se complete
      print("Tarea 1: recepción finalizada (%.3f, %.3f)" % (randNum2[0], randNum2[1]), flush=True)




      