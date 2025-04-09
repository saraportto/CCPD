#!/usr/bin/env python

"""
Para obtener tag y source en recepción, antes de la recepción se debe ejecutar
status = MPI.Status()

y usar el argumento adicional status=status en Recv. A continuación se pueden usar las
funciones status.Get_tag() y status.Get_source(). Probar el funcionamiento de esta
manera
"""

from mpi4py import MPI
import numpy as np

num_data = 4

comm = MPI.COMM_WORLD
my_rank = comm.rank
num_processes = comm.size

if my_rank != 0:
   data = np.arange(my_rank*100, my_rank*100+num_data, dtype=np.float64)
   comm.Send(data, dest=0, tag=500)
else:
   print("Hola, soy el proceso %d (hay %d procesos) y recibo:" % (my_rank, num_processes))
   for source_rank in range(1,num_processes):
      data = np.empty(num_data)

      status = MPI.Status()
      comm.Recv(data, status=status)
      source_rank = status.Get_source()

      print("Del proceso %d: " % source_rank, data)
