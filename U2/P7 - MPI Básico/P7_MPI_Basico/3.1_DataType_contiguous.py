#!/usr/bin/env python

import numpy as np
from mpi4py import MPI
from time import sleep

comm = MPI.COMM_WORLD
world_size = comm.Get_size()
rank = comm.Get_rank()

height = 6
width  = 6

num_of_data = 2 # Nº de bloques a enviar/recibir
pos_of_data = [2, 3] # Posición del bloque a enviar/recibir

row_type = MPI.INT64_T.Create_contiguous(count = 6) # Tipo básico: int64
row_type.Commit()

if rank == 0:
    send_array = (100+np.arange(width*height,dtype=np.int64)).reshape(height,width)
    print("Array on sender:")
    print(send_array)
    print()

    for i in range(0, len(pos_of_data)):
        comm.Send([send_array, (num_of_data, pos_of_data[i]), row_type], dest = 1)
    
if rank == 1:
    rec_array = np.zeros(width*height, dtype = np.int64).reshape(height, width)
    comm.Recv([rec_array, (num_of_data, pos_of_data[0]), row_type])
    sleep(1)
    print("Array on receiver:")
    print(rec_array)
    