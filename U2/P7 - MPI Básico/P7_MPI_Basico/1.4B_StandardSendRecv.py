#!/usr/bin/env python

"""
Modificar el programa inicial de tal forma que cada proceso de rango i mande un mensaje
al proceso de rango i+1 (el último debe mandar el mensaje al proceso de rango 0). 
No usar el argumento source en recepción. 

¿Qué pasa si el programa se ejecuta solamente con un proceso? 
¿Estaremos en envío síncrono o tamponado?
"""

from mpi4py import MPI
import numpy as np

num_data = 4

comm = MPI.COMM_WORLD
my_rank = comm.rank
num_processes = comm.size

data = np.arange(my_rank*100, my_rank*100+num_data, dtype=np.float64)

next_rank = (my_rank + 1) % num_processes
prev_rank = (my_rank - 1) % num_processes

comm.Send(data, dest=my_rank+1 , tag=500)

data = np.empty(num_data)
status = MPI.Status()
comm.Recv(data, status=status, source=prev_rank)

print("Hola, soy el proceso %d y recibo, " % my_rank, "del proceso %d : " % status.Get_source(), data)
