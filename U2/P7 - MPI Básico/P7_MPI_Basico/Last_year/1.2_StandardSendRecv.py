#!/usr/bin/env python

from mpi4py import MPI
import numpy as np

num_data = 4

comm = MPI.COMM_WORLD
my_rank = comm.rank
num_processes = comm.size

data = np.arange(my_rank*100, my_rank*100+num_data, dtype=np.float64)

if my_rank != num_processes - 1:
   comm.Send(data, dest=my_rank+1 , tag=500)

else:
   comm.Send(data, dest=0, tag=500)


data = np.empty(num_data)
status = MPI.Status()
comm.Recv(data, status=status)

print("Hola, soy el proceso %d y recibo, " % my_rank, "del proceso %d : " % status.Get_source(), data)