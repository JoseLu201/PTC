# capturar.py
import vrep
import os
import json
import time
import numpy as np
import cv2

# Función para realizar la captura de datos
def capturar_datos(cerca,media,lejos,manager, situation_folder, filename, iterations=50, sleep_time=0.5):
    
    _, resolution, image = vrep.simxGetVisionSensorImage(manager.clientID, manager.camhandle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)
    if (os.path.isdir(situation_folder)):
        print("Error: ya existe el directorio "+ situation_folder)
        os.chdir(situation_folder)
    else:
        os.mkdir(situation_folder)
        os.chdir(situation_folder)
        print("Cambiando el directorio de trabajo: ", os.getcwd())
    
    _, position = vrep.simxGetObjectPosition(manager.clientID, manager.personhandle, -1, vrep.simx_opmode_oneshot_wait)

    if position[0] <= cerca:
        rango1 = cerca
        rango2 = media
    elif media <= position[0] < lejos:
        rango1 = media
        rango2 = lejos
    else:
        rango1 = lejos
        rango2 = lejos + 1
        
    print("Destancias", cerca,media,lejos)
    print(f"POSICION INICIAL: {position}")
    print(f"RANGO1 : {rango1} | RANGO2 : {rango2}")
    # Crear el fichero JSON para guardar los datos del láser
    cabecera = {"TiempoSleep": sleep_time, "MaxIteraciones": iterations}
    with open(filename, "w") as fichero_laser:
        fichero_laser.write(json.dumps(cabecera) + '\n')
    
        
        rotation = 0
        for point in generate_random_points(iterations, (rango1,rango2), (position[1],-position[1])):
            vrep.simxSetObjectOrientation(manager.clientID, manager.personhandle, -1, [0.0, 0.0 ,3.05-(0.20)*rotation], vrep.simx_opmode_oneshot)
            rotation += 1

            vrep.simxSetObjectPosition(manager.clientID,manager.personhandle,-1,[point[0], point[1], 0.0],vrep.simx_opmode_oneshot)
            
            #Cambiamos la orientacion, ojo está en radianes: Para pasar de grados a radianes hay que multiplicar por PI y dividir por 180
            vrep.simxSetObjectOrientation(manager.clientID, manager.personhandle, -1, [0.0, 0.0 ,3.05-(0.20)*rotation], vrep.simx_opmode_oneshot)
            
            puntosx = []  # Lista para coordenadas x
            puntosy = []  # Lista para coordenadas y
            puntosz = []  # Lista para coordenadas z
            _, signalValue = vrep.simxGetStringSignal(manager.clientID, 'LaserData', vrep.simx_opmode_buffer)
            datosLaser = vrep.simxUnpackFloats(signalValue)
            
            # Procesar datos del láser
            for indice in range(0, len(datosLaser), 3):
                puntosx.append(datosLaser[indice + 1])
                puntosy.append(datosLaser[indice + 2])
                puntosz.append(datosLaser[indice])
                
            # Guardar los puntos x, y en el fichero JSON
            lectura = {"Iteracion": rotation, "PuntosX": puntosx, "PuntosY": puntosy}
            print(f"Iteracion: {rotation}")
            fichero_laser.write(json.dumps(lectura) + '\n')

            # Guardar frame de la cámara
            if rotation == 1 or rotation == iterations:
                _, resolution, image=vrep.simxGetVisionSensorImage(manager.clientID, manager.camhandle, 0, vrep.simx_opmode_buffer)
                print("Imagen: ")
                
                try:
                    img = np.array(image, dtype=np.uint8)
                    img.resize([resolution[0], resolution[1], 3])
                    img = np.rot90(img, 2)
                    img = np.fliplr(img)
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
                    # Salvar a disco la imagen
                    print(f'./Iteracion{rotation}.jpg')
                    print(len(img))
                    cv2.imwrite(f'./Iteracion{rotation}.jpg', img)
                except Exception:
                    print("Error intentando montar la imagen")
                    pass
                

            # Esperar
            time.sleep(sleep_time)

    # Cambiar de nuevo al directorio original
    os.chdir('../..')
    
def generate_random_points(num_points, x_range, y_range):
    # Generar coordenadas x e y aleatorias uniformes
    x_coords = np.random.uniform(x_range[0], x_range[1], num_points)
    y_coords = np.random.uniform(y_range[0], y_range[1], num_points)

    points = list(zip(x_coords, y_coords))

    return points