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

column_type = MPI.FLOAT.Create_vector(count=height, blocklength=height, stride=width)
column_type.Commit()

if rank == 0:
    send_array = (10 + np.arange(width * height, dtype=np.float32)).reshape(height, width)
    send_rows = np.zeros((2, width), dtype=np.float32)
    send_rows[0] = send_array[pos_of_data[0]]
    send_rows[1] = send_array[pos_of_data[1]]
    send_columns = np.zeros((height, 2), dtype=np.float32)
    send_columns[:, 0] = send_array[:, 2]  # Columna 2
    send_columns[:, 1] = send_array[:, 3]  # Columna 3
    comm.Send([send_rows, (num_of_data, None), row_type], dest=1)
    comm.Send([send_columns, (num_of_data, None), column_type], dest=1)
    print("Array on sender:")
    print(send_array)
    print()

if rank == 1:
    rec_rows = np.zeros((2, width), dtype=np.float32)
    rec_columns = np.zeros((height, 2), dtype=np.float32)
    comm.Recv([rec_rows, (num_of_data, None), row_type])
    comm.Recv([rec_columns, (num_of_data, None), column_type])
    rec_array = np.zeros((height, width), dtype=np.float32)
    rec_array[pos_of_data[0]] = rec_rows[0]
    rec_array[pos_of_data[1]] = rec_rows[1]
    rec_array[:, 2] = rec_columns[:, 0]  # Colocar la columna recibida en la columna 2 de la matriz de ceros
    rec_array[:, 3] = rec_columns[:, 1]  # Colocar la columna recibida en la columna 3 de la matriz de ceros
    sleep(1)
    print("Array on receiver:")
    print(rec_array)
