#! /usr/bin/env python3
from mpi4py import MPI
import sys

com = MPI.COMM_WORLD
numProcs = com.Get_size()
miRango = com.Get_rank()

message = "saludos del proceso %d" % miRango

port = MPI.Lookup_name('servicio')
intercom=com.Connect(port,MPI.INFO_NULL,root=0)
print("Port name %s" % port)

numServ = intercom.Get_remote_size()
print("Soy el cliente %d y hay %d servidores " % (miRango,numServ))

for i in range(numServ):
    intercom.send(message,i)



### ------- CONSOLA --------- ###
# $ \rm -f /tmp/ompi-server.txt
# $ killall ompi-server
# $ ompi-server -r /tmp/ompi-server.txt
# $ mpiexec --ompi-server file:/tmp/ompi-server.txt -np 2 ./37-ConnectServerProc.py
# Puerto abierto:  74252289.0:2767943890
# Soy el servidor 1 y hay 3 clientes
# Soy el servidor 0 y hay 3 clientes
# Soy el servidor 0, y recibo: saludos del proceso 0
# Soy el servidor 0, y recibo: saludos del proceso 1
# Soy el servidor 0, y recibo: saludos del proceso 2
# Soy el servidor 1, y recibo: saludos del proceso 0
# Soy el servidor 1, y recibo: saludos del proceso 1
# Soy el servidor 1, y recibo: saludos del proceso 2
# $
### ------------------------- ###

