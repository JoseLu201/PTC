import numpy as np
import pandas as pd
import pickle
import json
import matplotlib.pyplot as plt

# Calcular el punto medio entre dos centroides
def calcular_punto_medio(centroide1, centroide2):
    return {"x": (centroide1["x"] + centroide2["x"]) / 2, "y": (centroide1["y"] + centroide2["y"]) / 2}

# Calcular el centroide de un conjunto de puntos
def calcular_centroide(puntosX, puntosY):
    return {"x": np.mean(puntosX), "y": np.mean(puntosY)}



# Visualizar los resultados
def visualizar_resultados(df_test, prediccion):
    plt.figure()

    indices_unos = np.where(prediccion == 1)[0]
    colores = ['blue', 'green', 'purple', 'orange']
    
    for i in range(0, len(indices_unos) - 1, 2):
        index1 = indices_unos[i]
        index2 = indices_unos[i + 1]
        centroide1 = calcular_centroide(df_test.at[index1, 'puntosX'], df_test.at[index1, 'puntosY'])
        centroide2 = calcular_centroide(df_test.at[index2, 'puntosX'], df_test.at[index2, 'puntosY'])
    
        punto_medio = calcular_punto_medio(centroide1, centroide2)

        # Visualizar el punto medio con un color diferente para cada par
        plt.scatter(punto_medio["x"], punto_medio["y"], c=colores[i % len(colores)], marker='x', s=100)

    # Visualizar los clusters
    for cluster, color in zip(df_test.itertuples(), prediccion):
        if color == 1:
            plt.scatter(cluster.puntosX, cluster.puntosY, c='red', cmap='coolwarm', vmin=0, vmax=1)
        else:
            plt.scatter(cluster.puntosX, cluster.puntosY, c='blue', cmap='coolwarm', vmin=0, vmax=1)

    legend_pies = plt.scatter([], [], c='red', label='Piernas', cmap='coolwarm', vmin=0, vmax=1)
    legend_no_pies = plt.scatter([], [], c='blue', label='No Piernas', cmap='coolwarm', vmin=0, vmax=1)

    # Añadir leyenda
    plt.legend(handles=[legend_pies, legend_no_pies])
    plt.xlabel('Puntos X')
    plt.ylabel('Puntos Y')
    plt.title('Predicción de piernas.')
    plt.grid(True)
    plt.savefig("./casos/prediccion/prediccion.png")

    plt.show()
    
# Cargar el clasificador entrenado
def predecir(clasificador_file, caracteristicas, puntos):
    with open(clasificador_file, "rb") as archivo:
        clasificador = pickle.load(archivo)
    
    with open(puntos, 'r') as file:
        p = json.load(file)
    
    df_test = pd.DataFrame(p)
    
    with open(caracteristicas, 'r') as file:
        lines = file.readlines()
        print()
    clusters = [json.loads(line) for line in lines]
    
    # Convert the list of dictionaries to a DataFrame
    df_laser = pd.DataFrame(clusters)
    # print(df_test[0])
    # Extraer las características y la clase
    caracteristicas = df_laser[['perimetro', 'profundidad', 'anchura']]
    
    
    # Hacer la predicción
    prediccion = clasificador.predict(caracteristicas)
    print("Resultados de la predicción:")
    print(prediccion)
    
    # # Obtener índices donde la predicción es 1
    # indices_unos = np.where(prediccion == 1)[0]

    # # Iterar sobre las parejas de unos y calcular el punto medio
    # for i in range(len(indices_unos) - 1):
    #     index1 = indices_unos[i]
    #     index2 = indices_unos[i + 1]
    #     print("X: ")
    #     print(df_test.at[index1, 'puntosX'])
    #     centroide1 = calcular_centroide(df_test.at[index1, 'puntosX'], df_test.at[index1, 'puntosY'])
    #     centroide2 = calcular_centroide(df_test.at[index2, 'puntosX'], df_test.at[index2, 'puntosY'])

    #     punto_medio = calcular_punto_medio(centroide1, centroide2)

    #     # Visualizar el punto medio
    #     plt.scatter(punto_medio["x"], punto_medio["y"], c='red', marker='x', s=100)


    
    # for cluster, color in zip(df_test.itertuples(), prediccion):
    #     plt.scatter(cluster.puntosX, cluster.puntosY, c=[color] * len(cluster.puntosX),  cmap='coolwarm',vmin=0, vmax=1)

    # plt.xlabel('Puntos X')
    # plt.ylabel('Puntos Y')
    # plt.title('Predicción de piernas.')
    # plt.grid(True)
    # plt.legend()
    # plt.show()
    
    visualizar_resultados(df_test, prediccion)
    
    
    # Guardar los resultados en un archivo CSV
    #resultado.to_csv('resultados_prediccion.csv', index=False)
