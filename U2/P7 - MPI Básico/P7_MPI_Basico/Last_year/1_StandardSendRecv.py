#!/usr/bin/env python

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
      #comm.Recv(data)
      # 0 - comm.Recv(data, source=source_rank, tag=500)
      print("Del proceso %d, " % status.Get_source(), "tag=%d :" % status.Get_tag(), data,)