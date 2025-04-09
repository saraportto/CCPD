#!/usr/bin/env python
from mpi4py import MPI

# INICIALIZACIÓN MPI
com = MPI.COMM_WORLD
miRango = com.Get_rank()
numProcs = com.Get_size()

# SOLO con 7 procesos o más
if numProcs < 7:
    if miRango == 0:
        print("ERROR: lanzar el programa con 7 procesos o más")
    quit()

# GRUPO1: pares
if miRango % 2 == 0:
    grupo1 = com.Get_group().Incl(range(0, numProcs, 2))  
else:
    grupo1 = com.Get_group().Incl([]) # Grupo vacío

# GRUPO2: algunos procesos
if miRango in [2, 3, 4, 5]:
    grupo2 = com.Get_group().Incl([2, 3, 4, 5])  
else:
    grupo2 = com.Get_group().Incl([]) # Grupo vacío

# GRUPO INTERSECCIÓN
grupoIntersec = MPI.Group.Intersection(grupo1, grupo2)

# COMUNICADOR INTERSECCIÓN
comIntersec = com.Create(grupoIntersec)

# PRINTS de QUÉ procesos están en la INTERSECCIÓN
if comIntersec != MPI.COMM_NULL:
    miRangoIntersec = comIntersec.Get_rank()
    numProcsIntersec = comIntersec.Get_size()
    print(f"Proceso {miRango} en intersección ({miRangoIntersec}/{numProcsIntersec})")

else:
    print(f"Proceso {miRango} no en intersección")


###  ------- CONSOLA ------- ###
# $ mpirun -np 8 python 13B-IntracommsIntersec.py
# Proceso 7 no en intersección
# Proceso 5 no en intersección
# Proceso 3 no en intersección
# Proceso 2 en intersección (0/2)
# Proceso 6 no en intersección
# Proceso 0 no en intersección
# Proceso 1 no en intersección
# Proceso 4 en intersección (1/2)

### ----------------------- ###


