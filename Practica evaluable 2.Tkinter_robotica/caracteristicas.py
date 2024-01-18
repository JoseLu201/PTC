import json
import csv
import pandas as pd

def calcular_perimetro(puntos):
    # Calcular el perímetro sumando las distancias
    perimetro = sum(distancia(puntos[i], puntos[i + 1]) for i in range(len(puntos) - 1))
    return perimetro

def calcular_profundidad(puntos):
    # Calcular la profundidad como la distancia máxima de la recta P1Pn a los puntos P1 a Pn
    punto_inicial, punto_final = puntos[0], puntos[-1]
    recta = calcular_recta(punto_inicial, punto_final)
    profundidad = max(distancia_punto_recta(punto, recta) for punto in puntos)
    return profundidad

def calcular_anchura(puntos):
    # Calcular la anchura como la distancia de P1 a Pn
    anchura = distancia(puntos[0], puntos[-1])
    return anchura

def distancia(punto1, punto2):
    # Calcular la distancia euclidiana entre dos puntos
    return ((punto1[0] - punto2[0])**2 + (punto1[1] - punto2[1])**2)**0.5

def calcular_recta(punto1, punto2):
    # Calcular la recta que pasa por dos puntos
    pendiente = (punto2[1] - punto1[1]) / (punto2[0] - punto1[0])
    ordenada_origen = punto1[1] - pendiente * punto1[0]
    return pendiente, ordenada_origen

def distancia_punto_recta(punto, recta):
    # Calcular la distancia de un punto a una recta
    pendiente, ordenada_origen = recta
    distancia = abs(pendiente * punto[0] - punto[1] + ordenada_origen) / (pendiente**2 + 1)**0.5
    return distancia

def generar_caracteristicas_clusters(archivo_clusters, archivo_salida, es_pierna):
    caracteristicas = []

    with open(archivo_clusters, 'r') as file:
        lines = file.readlines()


    clusters = [json.loads(line) for line in lines]
    df = pd.DataFrame(clusters)
    
    for index, row in df.iterrows():
        
        # print("-------------------------------")
        cluster = row[0]
        if cluster != None:
            puntos = list(zip(cluster['puntosX'], cluster['puntosY']))
    
            perimetro = calcular_perimetro(puntos)
            profundidad = calcular_profundidad(puntos)
            anchura = calcular_anchura(puntos)
    
            caracteristicas.append({
                "numero_cluster": cluster["numero_cluster"],
                "perimetro": perimetro,
                "profundidad": profundidad,
                "anchura": anchura,
                "esPierna": es_pierna
            })

    with open(archivo_salida, 'w') as file:
        for caracteristica in caracteristicas:
            file.write(json.dumps(caracteristica) + '\n')


def generar_caracteristicas_clusters_predict(archivo_clusters, archivo_salida):
    caracteristicas = []

    with open(archivo_clusters, 'r') as file:
       clusters = json.load(file)
    df = pd.DataFrame(clusters)
    
    for index, row in df.iterrows():
        
        cluster = row
        puntos = list(zip(cluster['puntosX'], cluster['puntosY']))

        perimetro = calcular_perimetro(puntos)
        profundidad = calcular_profundidad(puntos)
        anchura = calcular_anchura(puntos)

        caracteristicas.append({
            "numero_cluster": cluster["numero_cluster"],
            "perimetro": perimetro,
            "profundidad": profundidad,
            "anchura": anchura
        })

    with open(archivo_salida, 'w') as file:
        for caracteristica in caracteristicas:
            file.write(json.dumps(caracteristica) + '\n')


def generar_dataset_csv(archivo_piernas, archivo_no_piernas, archivo_salida):
    with open(archivo_salida, 'w', newline='') as file:
        writer = csv.writer(file)

        # Escribir ejemplos negativos (clase 0)
        with open(archivo_no_piernas) as file_no_piernas:
            for line in file_no_piernas:
                caracteristica = json.loads(line)
                writer.writerow([caracteristica["perimetro"], caracteristica["profundidad"],
                                 caracteristica["anchura"], 0])

        # Escribir ejemplos positivos (clase 1)
        with open(archivo_piernas) as file_piernas:
            for line in file_piernas:
                caracteristica = json.loads(line)
                writer.writerow([caracteristica["perimetro"], caracteristica["profundidad"],
                                 caracteristica["anchura"], 1])
