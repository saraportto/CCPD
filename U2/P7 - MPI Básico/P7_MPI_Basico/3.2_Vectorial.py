#!/usr/bin/env python

import numpy as np
from mpi4py import MPI
from time import sleep

comm = MPI.COMM_WORLD
world_size = comm.Get_size()
rank = comm.Get_rank()

height = 6
width  = 6
num_of_data = 2  # No. bloques a enviar/recibir

column_type = MPI.FLOAT.Create_vector(count=2, blocklength=height, stride=width)
column_type.Commit()

if rank == 0:
    send_array = (10 + np.arange(width * height, dtype=np.float32)).reshape(height, width)
    send_columns = np.zeros((height, 2), dtype=np.float32)
    send_columns[:, 0] = send_array[:, 2]  # Columna 2
    send_columns[:, 1] = send_array[:, 3]  # Columna 3
    comm.Send([send_columns, (num_of_data, None), column_type], dest=1)
    print("Array on sender:")
    print(send_array)
    print()

if rank == 1:
    rec_columns = np.zeros((height, 2), dtype=np.float32)
    comm.Recv([rec_columns, (num_of_data, None), column_type])
    rec_array = np.zeros((height, width), dtype=np.float32)
    rec_array[:, 2] = rec_columns[:, 0]  # Colocar la columna recibida en la columna 2 de la matriz de ceros
    rec_array[:, 3] = rec_columns[:, 1]  # Colocar la columna recibida en la columna 3 de la matriz de ceros
    sleep(1)
    print("Array on receiver:")
    print(rec_array)
