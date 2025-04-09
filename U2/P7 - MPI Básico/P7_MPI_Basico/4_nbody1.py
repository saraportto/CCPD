#!/usr/bin/env python
import numpy as np

# 
DATAFILE = "data4sat.txt"
G = 6.674e-11 # constante gravitacional 
NUM_ITER  = 100001 # número de iteraciones
NUM_ITER_SHOW = 5000 # numero de iteraciones que se muestran
verbose = False # info adicional?

with open(DATAFILE, 'r') as file:
    noOfObjects = int(file.readline().strip())
    print("Number of objects:",noOfObjects)
    print()

    # Inicialización de arrays para posición, velocidad y masa
    x = np.zeros(noOfObjects)  # posición en x (m)
    y = np.zeros(noOfObjects)  # posición en y (m)
    vx = np.zeros(noOfObjects) # velocidad en x (m/s)
    vy = np.zeros(noOfObjects) # velocidad en y (m/s)
    m = np.zeros(noOfObjects)  # masa (kg)

    for i in range(noOfObjects):
        x[i] = float(file.readline().strip())
        y[i] = float(file.readline().strip())
        vx[i] = float(file.readline().strip())
        vy[i] = float(file.readline().strip())
        m[i] = float(file.readline().strip())

for niter in range(NUM_ITER):

    x_new = np.copy(x)
    y_new = np.copy(y)
    vx_new = np.copy(vx)
    vy_new = np.copy(vy)

    showData = False
    if niter % NUM_ITER_SHOW == 0:
        showData = True
        print("***** ITERATION {} *****".format(niter))

    for i in range(noOfObjects):
        ax_total = 0.0
        ay_total = 0.0

        for j in range(noOfObjects):
            if i == j:
                continue

            # Calcular diferencia de posiciones
            dx = x[j] - x[i]
            dy = y[j] - y[i]
            # Calcular la distancia entre los objetos
            d = np.sqrt(dx**2 + dy**2)
            # Calcular la magnitud de la fuerza gravitatoria
            f = G * m[i] * m[j] / d**2
            # Calcular las componentes de la fuerza en x e y
            fx = f * dx / d
            fy = f * dy / d
            # Calcular la aceleración sobre el objeto i (F = m*a => a = F/m)
            ax = fx / m[i]
            ay = fy / m[i]

            if showData and verbose:
                print("  Distance between objects {} and {}: {:.1f} m".format(i+1, j+1, d))
                print("  Force between objects {} and {}: {:.3f} N".format(i+1, j+1, f))
                print("  Force along x axis on object {} made by object {}: {:.3f} N".format(i+1, j+1, fx))
                print("  Acceleration along x axis on object {} made by object {}: {:.3f} m/s²".format(i+1, j+1, ax))
                print("  Force along y axis on object {} made by object {}: {:.3f} N".format(i+1, j+1, fy))
                print("  Acceleration along y axis on object {} made by object {}: {:.3f} m/s²".format(i+1, j+1, ay))

            ax_total += ax
            ay_total += ay

        # Actualización de velocidades y posiciones (integración tipo Euler)
        vx_new[i] += ax_total
        vy_new[i] += ay_total

        x_new[i] += vx_new[i]
        y_new[i] += vy_new[i]

        if showData:
            print("New position of object {}: {:.2f}, {:.2f}".format(i, x_new[i], y_new[i]))

    # Se actualizan las variables para la siguiente iteración
    x = np.copy(x_new)
    y = np.copy(y_new)
    vx = np.copy(vx_new)
    vy = np.copy(vy_new)

# ------------------------------------------------------------------
#   mpirun -np 4 ./GravitSerie.py
# ------------------------------------------------------------------