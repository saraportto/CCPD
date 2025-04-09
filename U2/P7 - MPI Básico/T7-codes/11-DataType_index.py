#!/usr/bin/env python

import numpy as np
from mpi4py import MPI
from time import sleep

# INICIALIZACIÓN MPI
comm = MPI.COMM_WORLD
world_size = comm.Get_size()
rank = comm.Get_rank()

# DATOS MATRIZ
height = 5 # altura
width  = 5 # anchura

# DATOS PARA ENVÍO Y RECEPCIÓN
num_of_data = 1 # Nº de bloques a enviar/recibir

# CREACIÓN TIPO DE DATO
blocks_type = MPI.DOUBLE.Create_indexed([1,2,3], [0,4,12])
# blocklengths: nº etos que hay en cada bloque (varios)
# displacements: desplazamiento relativo (contando desde 0)
# Tipo básico float64

blocks_type.Commit() # commit tipo


# PRCESO RANGO 0 ENVÍA
if rank == 0:
    send_array = (10+np.arange(width*height,dtype=np.float64)).reshape(height,width)
    comm.Send([send_array, (num_of_data, None), blocks_type], dest = 1)
    # send array:   [array de envío;   num-data, pos-data;   tipo de dato]
    # dest: proceso rango 1

    print("Array on sender:")
    print(send_array)
    print()

# PROCESO RANGO 1 RECIBE
if rank == 1:
    rec_array = np.zeros(width*height, dtype = np.float64).reshape(height, width)
    comm.Recv([rec_array, (num_of_data, None), blocks_type])
    # rec array:    [array de ceros;   num-data, pos-data;   tipo de dato]

    sleep(1)
    print("Array on receiver:")
    print(rec_array)
    

### ------- CONSOLA ------- ###
# (mpi) $ mpirun -np 2 ./11-DataType_index.py
#
# Array on sender:
# [[10. 11. 12. 13. 14.]
# [15. 16. 17. 18. 19.]
# [20. 21. 22. 23. 24.]
# [25. 26. 27. 28. 29.]
# [30. 31. 32. 33. 34.]]
#
# Array on receiver:
# [[10. 0. 0. 0. 14.]
# [15. 0. 0. 0. 0.]
# [ 0. 0. 22. 23. 24.]
# [ 0. 0. 0. 0. 0.]
# [ 0. 0. 0. 0. 0.]]

### ---------------------- ###
