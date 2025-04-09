#!/usr/bin/env python

from mpi4py import MPI

# INICIALIZACIÓN MPI
comm = MPI.COMM_WORLD
my_rank = comm.rank
num_processes = comm.size

# ENVÍO DE DATOS (todos los procesos menos el 0)
if my_rank != 0:
   data = "Saludos del proceso {}".format(my_rank)
   comm.send(data, dest=0, tag=500) # envío de data al proceso 0

# RECEPCIÓN DE DATOS (proceso 0)
else:
   print("Hola, soy el proceso %d (hay %d procesos) y recibo:" % (my_rank, num_processes))

   # Bucle de recepción de datos
   for source_rank in range(1,num_processes):   
      data = comm.recv(source=source_rank, tag=500) # recibe en data lo que le envía el proceso source_rank
      print(data)

      