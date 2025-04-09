#!/usr/bin/env python

"""
Ejecutar el programa 01-StandardSendRecv.py cambiando el número de procesos.
Observar la salida
"""

from mpi4py import MPI
import numpy as np

# TAMAÑO BUFFER ENVÍO
num_data = 4

# INICIALIZACIÓN MPI
comm = MPI.COMM_WORLD # comunicador global
my_rank = comm.rank # rango del proceso
num_processes = comm.size # número de procesos

# ENVÍO DE DATOS (todos los procesos menos el 0)
if my_rank != 0:
   data = np.arange(my_rank*100, my_rank*100+num_data, dtype=np.float64) # array de envío
   comm.Send(data, dest=0, tag=500) # envío de data al proceso 0

# RECEPCIÓN DE DATOS (proceso 0)
else:
   print("Hola, soy el proceso %d (hay %d procesos) y recibo:" % (my_rank, num_processes))

   # Bucle de recepción de datos
   for source_rank in range(1,num_processes): 
      data = np.empty(num_data) # crea un buffer vacío
      comm.Recv(data, source=source_rank, tag=500) # recibe en data lo que le envía el proceso source_rank
      print("Del proceso %d: " % source_rank, data)

