import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score, GridSearchCV
import pickle

def entrenar_clasificador(class_file, data_path="piernasDataset.csv"):
    # Cargar el conjunto de datos
    df = pd.read_csv(data_path, header=None, names=["perimetro", "profundidad", "anchura", "clase"])

    # Dividir los datos en características (X) y etiquetas (y)
    X = df.drop("clase", axis=1)
    y = df["clase"]

    # Dividir el conjunto de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Inicializar el clasificador SVM
    svc = SVC()

    # Entrenar el clasificador
    svc.fit(X_train, y_train)

    # Hacer predicciones en el conjunto de prueba
    y_pred = svc.predict(X_test)

    # Evaluar el rendimiento
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)

    print(f"Accuracy: {accuracy}")
    print("Confusion Matrix:")
    print(conf_matrix)
    print("Classification Report:")
    print(classification_rep)

    # Validación cruzada
    scores = cross_val_score(svc, X, y, cv=5)
    print(f"Cross-Validation Accuracy: {scores.mean()} (+/- {scores.std() * 2})")

    # Búsqueda de hiperparámetros
    param_grid = {'C': [0.1, 1, 10, 100], 'kernel': ['linear', 'rbf', 'poly']}
    grid_search = GridSearchCV(SVC(), param_grid, cv=5, verbose=2)
    grid_search.fit(X, y)

    print("Mejores parámetros encontrados:")
    print(grid_search.best_params_)
    
    # Mostrar resultados para cada combinación de kernel
    results_df = pd.DataFrame(grid_search.cv_results_)
    print("Resultados detallados:")
    print(results_df[['param_kernel', 'mean_test_score', 'std_test_score', 'rank_test_score']])
    
    # Comparar rendimiento de kernels
    mean_scores = results_df.groupby('param_kernel')['mean_test_score'].mean()
    print("Rendimiento promedio de cada kernel:")
    print(mean_scores)
    
    mejor_kernel = mean_scores.idxmax()
    print(f"\nMejor kernel: {mejor_kernel}")

    best_svc = grid_search.best_estimator_
    best_svc.fit(X_train, y_train)
    
    # Hacer predicciones en el conjunto de prueba
    y_pred = best_svc.predict(X_test)

    # Evaluar el rendimiento
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)
    
    print(f"Accuracy: {accuracy}")
    print("Confusion Matrix:")
    print(conf_matrix)
    print("Classification Report:")
    print(classification_rep)
    
    # Validación cruzada con el mejor clasificador
    scores = cross_val_score(best_svc, X, y, cv=5)
    print(f"Cross-Validation Accuracy: {scores.mean()} (+/- {scores.std() * 2})")

    # Guardar el clasificador
    with open(class_file, "wb") as archivo:
        pickle.dump(best_svc, archivo)


