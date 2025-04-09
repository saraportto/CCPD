#!/usr/bin/env python

import numpy as np
from mpi4py import MPI
from time import sleep

# INICIALIZACIÓN MPI
comm = MPI.COMM_WORLD
world_size = comm.Get_size()
rank = comm.Get_rank()

# DATOS MATRIZ
height = 6
width  = 6

# DATOS PARA ENVÍO Y RECEPCIÓN
num_of_data = 1 # Nº de bloques a enviar/recibir
pos_of_data = 2 # Posición del bloque a enviar/recibir

# CREACIÓN TIPO CONTIGUO

row_type = MPI.INT64_T.Create_contiguous(count = 6) 
# tipo básico: int64
# count: nº de elementos a enviar/recibir

row_type.Commit() # Comitear tipo


# PROCESO RANGO 0 ENVÍA
if rank == 0:
    send_array = (100+np.arange(width*height,dtype=np.int64)).reshape(height,width)
    print("Array on sender:")
    print(send_array)
    print()
    comm.Send([send_array, (num_of_data, pos_of_data), row_type], dest = 1)
    # send array:   [array de envío;   num-data, pos-data;   tipo de dato]
    # dest: proceso rango 1
    

# PROCESO RANGO 1 RECIBE
if rank == 1:
    rec_array = np.zeros(width*height, dtype = np.int64).reshape(height, width)
    comm.Recv([rec_array, (num_of_data, pos_of_data), row_type])
    # rec array:    [array de ceros;   num-data, pos-data;   tipo de dato]
    sleep(1)
    print("Array on receiver:")
    print(rec_array)
    

### ------- CONSOLA ------- ###
# (mpi) $ mpirun -np 2 ./9-DataType_contiguous.py
#
# Array on sender:
# [[100 101 102 103 104 105]
# [106 107 108 109 110 111]
# [112 113 114 115 116 117]
# [118 119 120 121 122 123]
# [124 125 126 127 128 129]
# [130 131 132 133 134 135]]
#
# Array on receiver:
# [[ 0 0 0 0 0 0]
# [ 0 0 0 0 0 0]
# [112 113 114 115 116 117]
# [ 0 0 0 0 0 0]
# [ 0 0 0 0 0 0]
# [ 0 0 0 0 0 0]]

### ---------------------- ###


