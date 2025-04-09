#!/usr/bin/env python

import numpy as np
from mpi4py import MPI
from time import sleep

comm = MPI.COMM_WORLD
world_size = comm.Get_size()
rank = comm.Get_rank()

height = 6
width  = 6

num_of_data = 2  # Nº de bloques a enviar/recibir
pos_of_data = [2, 3]  # Posición del bloque a enviar/recibir

row_type = MPI.INT64_T.Create_contiguous(count=width)  # Tipo básico: int64
row_type.Commit()

if rank == 0:
    send_array = (10 + np.arange(width * height, dtype=np.int64)).reshape(height, width)
    print("Array on sender:")
    print(send_array)
    print()

    for pos in pos_of_data:
        comm.Send([send_array[pos], row_type], dest=1)

if rank == 1:
    rec_arrays = []

    for _ in range(num_of_data):
        rec_array = np.zeros(width, dtype=np.int64)
        comm.Recv([rec_array, row_type])
        rec_arrays.append(rec_array)
        sleep(1)

    result_array = np.zeros((height, width), dtype=np.int64)
    for i, pos in enumerate(pos_of_data):
        result_array[pos] = rec_arrays[i]

    print("Array on receiver:")
    print(result_array)
