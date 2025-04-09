#!/usr/bin/env python

import numpy as np
from mpi4py import MPI
from time import sleep

# INICIALIZACIÓN MPI
comm = MPI.COMM_WORLD
world_size = comm.Get_size()
rank = comm.Get_rank()

# DATOS MATRIZ
height = 5
width  = 5

# DATOS PARA ENVÍO Y RECEPCIÓN
num_of_data = 1 # No. bloques a enviar/recibir

# CREACIÓN TIPO DE DATO
checkerboard_type = MPI.FLOAT.Create_vector(count = 13, blocklength = 1, stride = 2)
# count: nº de bloques de elementos a enviar/recibir
# blocklength: nª elementos/bloque
# stride: nº etos entre primer elemento de cada bloque (salto)
# Tipo básico float32

checkerboard_type.Commit() # commit


# PROCESO RANGO 0 ENVÍA
if rank == 0:
    send_array = (10+np.arange(width*height,dtype=np.float32)).reshape(height,width) # array de envío
    comm.Send([send_array, (num_of_data, None), checkerboard_type], dest = 1)
    # send array:   [array de envío;   num-data, pos-data;   tipo de dato]
    # dest: proceso rango 1

    print("Array on sender:")
    print(send_array)
    print()


# PROCESO RANGO 1 RECIBE
if rank == 1:
    rec_array = np.zeros(width*height, dtype = np.float32).reshape(height, width) # array vacío recibir
    comm.Recv([rec_array, (num_of_data, None), checkerboard_type])
    # rec array:    [array de ceros;   num-data, pos-data;   tipo de dato]

    sleep(1)
    print("Array on receiver:")
    print(rec_array)


### ------- CONSOLA ------- ###
# (mpi) $ mpirun -np 2 ./10-DataType_vector.py
#
# Array on sender:
# [[10. 11. 12. 13. 14.]
# [15. 16. 17. 18. 19.]
# [20. 21. 22. 23. 24.]
# [25. 26. 27. 28. 29.]
# [30. 31. 32. 33. 34.]]
#
# Array on receiver:
# [[10. 0. 12. 0. 14.]
# [ 0. 16. 0. 18. 0.]
# [20. 0. 22. 0. 24.]
# [ 0. 26. 0. 28. 0.]
# [30. 0. 32. 0. 34.]]

### ---------------------- ###




    