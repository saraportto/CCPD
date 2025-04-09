#!/usr/bin/env python
import numpy as np
from mpi4py import MPI

DATAFILE = "data4sat.txt"
G = 6.674e-11
NUM_ITER = 100001
NUM_ITER_SHOW = 5000
verbose = False

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def read_and_distribute_data():
    if rank == 0:
        with open(DATAFILE, 'r') as file:
            noOfObjects = int(file.readline().strip())
            print("Number of objects:", noOfObjects)
            print()

            data = []
            for _ in range(noOfObjects):
                obj_data = []
                obj_data.append(float(file.readline().strip()))  # x coordinate (m)
                obj_data.append(float(file.readline().strip()))  # y coordinate (m)
                obj_data.append(float(file.readline().strip()))  # x velocity (m/s)
                obj_data.append(float(file.readline().strip()))  # y velocity (m/s)
                obj_data.append(float(file.readline().strip()))  # mass (kg)
                data.append(obj_data)

            for i in range(1, size):
                comm.send(data[i - 1], dest=i)
    else:
        obj_data = comm.recv(source=0)
        return obj_data

def calculate_and_update(data):
    x, y, vx, vy, m = data

    for niter in range(NUM_ITER):
        x_new = x
        y_new = y
        vx_new = vx
        vy_new = vy

        for i in range(noOfObjects):
            ax_total = 0.0
            ay_total = 0.0

            for j in range(noOfObjects):
                if (i == j):
                    continue
                d = np.sqrt((data[j][0] - x) ** 2 + (data[j][1] - y) ** 2)
                f = G * m * data[j][4] / (d ** 2)
                fx = f * (data[j][0] - x) / d
                ax = fx / m
                fy = f * (data[j][1] - y) / d
                ay = fy / m

                ax_total += ax
                ay_total += ay

            vx_new += ax_total
            vy_new += ay_total

            x_new += vx_new
            y_new += vy_new

        if (niter % NUM_ITER_SHOW == 0):
            print("***** ITERATION {} *****".format(niter))
            for i in range(noOfObjects):
                print("New position of object {}: {:.2f}, {:.2f}".format(i, x_new[i], y_new[i]))

    return x_new, y_new, vx_new, vy_new

if __name__ == "__main__":
    data = read_and_distribute_data()

    updated_data = calculate_and_update(data)

    print("Final updated data for object {}:".format(rank))
    print("x:", updated_data[0])
    print("y:", updated_data[1])
    print("vx:", updated_data[2])
    print("vy:", updated_data[3])
