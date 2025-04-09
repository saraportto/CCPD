#!/usr/bin/env python

import numpy as np
from mpi4py import MPI
from time import sleep

comm = MPI.COMM_WORLD
world_size = comm.Get_size()
rank = comm.Get_rank()

height = 5
width  = 5
num_of_data = 1 # Nº de bloques a enviar/recibir

blocks_type = MPI.DOUBLE.Create_indexed([1,2,3], [0,4,12])
    # Tipo básico float64
blocks_type.Commit()

if rank == 0:
    send_array = (10+np.arange(width*height,dtype=np.float64)).reshape(height,width)
    comm.Send([send_array, (num_of_data, None), blocks_type], dest = 1)
    print("Array on sender:")
    print(send_array)
    print()

if rank == 1:
    rec_array = np.zeros(width*height, dtype = np.float64).reshape(height, width)
    comm.Recv([rec_array, (num_of_data, None), blocks_type])
    sleep(1)
    print("Array on receiver:")
    print(rec_array)
    