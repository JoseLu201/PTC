

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def distancia(punto1, punto2):
    # Función para calcular la distancia entre dos puntos
    return np.sqrt((punto1[0] - punto2[0])**2 + (punto1[1] - punto2[1])**2)

# Dada una lectura del laser, (puntos X e puntos Y) y las caractersiticas para genera  un cluster
def agrupar_puntos(puntos_x, puntos_y, min_puntos, max_puntos, umbral_distancia):
    clusters = []
    current_cluster = []

    for x, y in zip(puntos_x, puntos_y):
        punto = (x, y)

        if not current_cluster or distancia(current_cluster[-1], punto) <= umbral_distancia:
            current_cluster.append(punto)
        else:
            if min_puntos <= len(current_cluster) <= max_puntos:
                numero_cluster = len(clusters) + 1
                clusters.append({
                    "numero_cluster": numero_cluster,
                    "numero_puntos": len(current_cluster),
                    "puntosX": [p[0] for p in current_cluster],
                    "puntosY": [p[1] for p in current_cluster]
                })

            current_cluster = [punto]

    if min_puntos <= len(current_cluster) <= max_puntos:

        numero_cluster = len(clusters) + 1
        clusters.append({
            "numero_cluster": numero_cluster,
            "numero_puntos": len(current_cluster),
            "puntosX": [p[0] for p in current_cluster],
            "puntosY": [p[1] for p in current_cluster]
        })
    
    return clusters


def guardar_clusters_json(nombre_archivo, clusters):
    with open(nombre_archivo, 'a') as file:
        file.write(json.dumps(clusters) + '\n')

def plot_clusters(clusters):
    for cluster in clusters:
        plt.scatter(cluster["puntosX"], cluster["puntosY"], label=f'Cluster {cluster["numero_cluster"]}')

    plt.xlabel('Puntos X')
    plt.ylabel('Puntos Y')
    plt.grid(True)
    plt.legend()
    plt.show()
       
def agrupar_datos(file,min_puntos,max_puntos,umbral_distancia, out_file):
    with open(file, 'r') as file:
        lineas_resto = file.readlines()[1:]

    lista_dicts = [json.loads(line) for line in lineas_resto]
    df = pd.DataFrame(lista_dicts)
    cluster_list = []
    
    for index, row in df.iterrows():
        X = np.array([float(x) for x in row['PuntosX']])
        Y = np.array([float(y) for y in row['PuntosY']])

        cluster = agrupar_puntos(X,Y, min_puntos, max_puntos, umbral_distancia)

        guardar_clusters_json(out_file, cluster)
        cluster_list.append(cluster)
        # print("Iteracion: ", f['Iteracion'])
        
        # plot_clusters(cluster)

    return cluster_list

# clusters = main("./casos/positivo1/enPieCerca.json", min_puntos, max_puntos, umbral_distancia)
