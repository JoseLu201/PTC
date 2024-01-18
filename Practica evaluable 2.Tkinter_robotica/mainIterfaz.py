import tkinter as tk
from tkinter import messagebox
import vrep
import os
import json
import matplotlib.pyplot as plt
from vrep_manager import VrepManager
from capturar import capturar_datos
from agrupar import agrupar_datos
from caracteristicas import generar_caracteristicas_clusters, generar_dataset_csv, generar_caracteristicas_clusters_predict
from clasificarSVM import entrenar_clasificador
from predecir import predecir

# 4.8053e-01

class InterfazGrafica:
    def __init__(self, root, vrep_manager):
        self.root = root
        self.vrep_manager = vrep_manager
        self.root.geometry("700x300")
        self.root.title("Interfaz Gráfica")
        self.label_estado = tk.Label(self.root, text="Estado: No conectado a VREP")
        self.label_estado.grid(row=3, column=0)
        

        # Variables de parámetros
        self.iteraciones = tk.IntVar(value=50)
        self.cerca = tk.DoubleVar(value=0.5)
        self.media = tk.DoubleVar(value=1.5)
        self.lejos = tk.DoubleVar(value=2.5)
        self.min_points = tk.IntVar(value=3)
        self.max_points= tk.IntVar(value=50)
        self.umbral = tk.DoubleVar(value=.05)
        
        self.param_col = 1
        
        self.ficheros = self.load_files("./casos")
    
        # Crear elementos de la interfaz
        self.create_interface()
        
        self.debuggin = False
        self.connected_to_simulator = False
        
        self.cluster_file_piernas = "./casos/prediccion/clustersPiernas.json"
        self.cluster_file_no_piernas = "./casos/prediccion/clustersNoPiernas.json"
        
            
        self.caracteristicas_csv= "./casos/prediccion/piernasDataset.csv"
        
        self.dat_piernas = "./casos/prediccion/caracteristicasPiernas.dat"
        self.dat_no_piernas = "./casos/prediccion/caracteristicasNoPiernas.dat"
        
        self.lectura_file = "./casos/prediccion/data_test.json"
        self.agrupado_file = "./casos/prediccion/data_test_agrupado.json"
        self.caracteristicas_data = "./casos/prediccion/data_test_caracteristicas.dat"
        self.classificator_filename = "./casos/prediccion/clasificador_svm.pkl"
        
        crear_directorios()

    def create_interface(self):
        # Etiquetas
        tk.Label(self.root, text="Parámetros").grid(row=2, column=self.param_col)
        tk.Label(self.root, text="Fichero para la captura").grid(row=2, column=self.param_col+2)
        
        # Entradas de texto
        self.label_iters = tk.Label(self.root, text="Iteraciones:",anchor="e",width=15)
        self.label_iters.grid(row=3, column=self.param_col)
        self.iters_entry = tk.Entry(self.root, textvariable=self.iteraciones,width=10)
        self.iters_entry.grid(row=3, column=self.param_col+1)
        
        self.label_cerca = tk.Label(self.root, text="Cerca:",anchor="e",width=15)
        self.label_cerca.grid(row=4, column=self.param_col)
        self.cerca_entry = tk.Entry(self.root, textvariable=self.cerca,width=10)
        self.cerca_entry.grid(row=4, column=self.param_col+1)
        
        self.label_media = tk.Label(self.root, text="Media:", anchor="e",width=15)
        self.label_media.grid(row=5, column=self.param_col)
        self.media_entry = tk.Entry(self.root, textvariable=self.media,width=10)
        self.media_entry.grid(row=5, column=self.param_col+1)
        
        self.label_lejos= tk.Label(self.root, text="Lejos:",anchor="e",width=15)
        self.label_lejos.grid(row=6, column=self.param_col)
        self.lejos_entry = tk.Entry(self.root, textvariable=self.lejos,width=10)
        self.lejos_entry.grid(row=6, column=self.param_col+1)
        
        self.label_min_points = tk.Label(self.root, text="Min puntos:",anchor="e",width=15)
        self.label_min_points.grid(row=7, column=self.param_col)
        self.min_points_entry = tk.Entry(self.root, textvariable=self.min_points,width=10)
        self.min_points_entry.grid(row=7, column=self.param_col+1)
        
        self.label_max_points_entry = tk.Label(self.root, text="Max puntos:",anchor="e",width=15)
        self.label_max_points_entry.grid(row=8, column=self.param_col)
        self.max_points_entry = tk.Entry(self.root, textvariable=self.max_points,width=10)
        self.max_points_entry .grid(row=8, column=self.param_col+1)
        
        self.label_umbral = tk.Label(self.root, text="UmbralDistancia:",anchor="e",width=16)
        self.label_umbral.grid(row=9, column=self.param_col)
        self.umbral_entry = tk.Entry(self.root, textvariable=self.umbral,width=10)
        self.umbral_entry.grid(row=9, column=self.param_col+1)
        

        

        # Botones
        self.connect_button = tk.Button(self.root, text="Conectar con VREP", command=self.connect_vrep)
        self.connect_button.grid(row=1, column=0)
        
        self.disconnect_button = tk.Button(self.root, text="Desconectar y detener", state=tk.DISABLED, command=self.disconnect_vrep)
        self.disconnect_button.grid(row=2, column=0)

        self.capture_button = tk.Button(self.root, text="Capturar", state=tk.DISABLED, command=self.capture_data)
        self.capture_button.grid(row=4, column=0)
        
        self.group_button = tk.Button(self.root, text="Agrupar", state=tk.DISABLED, command=self.agrupar)
        self.group_button.grid(row=5, column=0)
        
        self.extraer_button = tk.Button(self.root, text="Exrteaer Caracteristicas", state=tk.DISABLED, command=self.extraer_caracteristicas)
        self.extraer_button.grid(row=6, column=0)
        
        self.train_button = tk.Button(self.root, text="Entrenar Clasificador", state=tk.DISABLED, command=self.entrenar_clasificador)
        self.train_button.grid(row=7, column=0)
        
        self.predecir_button = tk.Button(self.root, text="Predecir", state=tk.DISABLED, command=self.predecir)
        self.predecir_button.grid(row=8, column=0)
        
        self.exit_button = tk.Button(self.root, text="Salir", state=tk.ACTIVE, command=self.salir)
        self.exit_button.grid(row=9, column=0)
        
        self.change_button = tk.Button(self.root, text="Cambiar", state=tk.ACTIVE, command=self.change_data)
        self.change_button.grid(row=11, column=self.param_col)
        
        self.debug_button = tk.Button(self.root, text="DEBUG", state=tk.ACTIVE, command=self.debug)
        self.debug_button.grid(row=12, column=0)


        # Configurar el cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        
        #Panel derecho de archivos
        self.listbox_ficheros = tk.Listbox(self.root, width=35, height=12)
        for fichero in self.ficheros:
            self.listbox_ficheros.insert(tk.END, fichero)
            
        self.listbox_ficheros.grid(row=3 ,column=self.param_col+2, rowspan=6, sticky="nsew")
        


    def connect_vrep(self):
        if self.vrep_manager.conectar_vrep():
            self.vrep_manager.begin()
            print("Persona: ", self.vrep_manager.personhandle)
            self.label_estado.config(text="Estado: Conectado a VREP")
            self.disconnect_button["state"] = tk.NORMAL
            self.capture_button["state"] = tk.NORMAL
            self.connected_to_simulator = True
            
            # Borrar
            self.group_button["state"] = tk.NORMAL

    def disconnect_vrep(self):
        self.vrep_manager.desconectar_vrep()
        self.label_estado.config(text="Estado: No conectado a VREP")
        self.disconnect_button["state"] = tk.DISABLED
        self.capture_button["state"] = tk.DISABLED
        self.connected_to_simulator = False
        
    
    def capture_data(self):
        # Verificar si se seleccionó algún archivo
        seleccionado = self.listbox_ficheros.curselection()
        if not seleccionado:
            messagebox.showerror("Error", "Selecciona al menos un archivo antes de capturar.")
            return

        # Obtener el nombre del archivo seleccionado
        archivo_seleccionado = self.ficheros[seleccionado[0]]
        file_separado = archivo_seleccionado.rsplit('/',1)
        print(file_separado)
        
        full_file_path = os.path.join(file_separado[0], file_separado[1])

        if os.path.exists(full_file_path):
           confirm_overwrite = messagebox.askyesno("Confirmar", "El archivo ya existe. ¿Quieres sobrescribirlo?")
           if not confirm_overwrite:
               return
           
        capturar_datos(self.cerca.get(),self.media.get(), self.lejos.get(), self.vrep_manager, file_separado[0], file_separado[1], iterations=self.iteraciones.get())
        self.group_button["state"] = tk.NORMAL
        print("FIN DE CAPTURA")

    
    def agrupar(self):
        
        lista_pos = [f for f in self.ficheros if "positivo" in f]
        lista_neg = [f for f in self.ficheros if "negativo" in f]
        erase_file(self.cluster_file_piernas)
        erase_file(self.cluster_file_no_piernas)
       
        for f in lista_pos:
            print("Archivo: ", f)
            agrupar_datos(f, self.min_points.get(),self.max_points.get(),self.umbral.get(), self.cluster_file_piernas)

        for f in lista_neg:
            print("Archivo: ", f)
            agrupar_datos(f, self.min_points.get(),self.max_points.get(),self.umbral.get(), self.cluster_file_no_piernas)
        
        self.extraer_button["state"] = tk.NORMAL
        print("AGRUPAMIENTO completada")
            
        
    
    def extraer_caracteristicas(self):
        generar_caracteristicas_clusters(self.cluster_file_piernas, self.dat_piernas, es_pierna=True)
        generar_caracteristicas_clusters(self.cluster_file_no_piernas, self.dat_no_piernas, es_pierna=False)
        generar_dataset_csv(self.dat_piernas, self.dat_no_piernas, self.caracteristicas_csv)
        self.train_button["state"] = tk.NORMAL
        
        print("Extraccion Completada")
    
    def entrenar_clasificador(self):
        entrenar_clasificador(self.classificator_filename, self.caracteristicas_csv)
        
        self.predecir_button["state"] = tk.NORMAL
        
        print("Entrenamiento Completado")
        
    def predecir(self):
        
        puntosx=[] 
        puntosy=[]
        returnCode, signalValue = vrep.simxGetStringSignal(self.vrep_manager.clientID,'LaserData',vrep.simx_opmode_buffer) 
        
        # Desempaquetar los datos láser
        datosLaser = vrep.simxUnpackFloats(signalValue)

        for indice in range(0, len(datosLaser), 3):
            puntosx.append(datosLaser[indice + 1])
            puntosy.append(datosLaser[indice + 2])
    
    
        
        erase_file(self.agrupado_file)
        
        
        cabecera = {"Num_p": len(puntosx)}
        
        # Leo los datos
        with open(self.lectura_file , "w") as fichero_laser:
            fichero_laser.write(json.dumps(cabecera) + '\n')

            lectura = {"PuntosX": puntosx, "PuntosY": puntosy}
            fichero_laser.write(json.dumps(lectura) + '\n')
            plt.scatter(puntosx,puntosy)

            plt.xlabel('Puntos X')
            plt.ylabel('Puntos Y')
            # plt.xlim(0, 5)  
            # plt.ylim(-1.5, 1.5)
            plt.grid(True)
            plt.legend()
            plt.show()
        
        # Agrupo los datos en clusters
        agrupar_datos(self.lectura_file , self.min_points.get(),self.max_points.get(),self.umbral.get(), self.agrupado_file)
        
        # A paritr de esos clusters obtengo sus caracteristicas
        generar_caracteristicas_clusters_predict(self.agrupado_file, self.caracteristicas_data)
        
        predecir(self.classificator_filename, self.caracteristicas_data, self.agrupado_file)
        # predecir("prueba.pkl", caracteristicas_data, agrupado_file)        
    
    def salir(self):
        if self.connected_to_simulator:
            # Show warning message about disconnecting first
            messagebox.showwarning("Advertencia", "Debes desconectarte primero del simulador.")
            return  # Do not proceed to exit until disconnected

        # Ask user if they want to exit
        confirm_exit = messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?")
        if confirm_exit:            
            self.disconnect_vrep()
            self.on_closing()
        
    
    def change_data(self):
        self.iteraciones.set(self.iters_entry.get())
        self.cerca.set(self.cerca_entry.get())
        self.media.set(self.media_entry.get() )
        self.lejos.set(self.lejos_entry.get())
        self.min_points.set(self.min_points_entry.get())
        self.max_points.set(self.max_points_entry.get())
        self.umbral.set(self.umbral_entry.get())

        
        
    
    def debug(self):
        
        self.debuggin = not self.debuggin
        if self.debuggin:
            self.last_button_state = {
                "connect": self.connect_button["state"],
                "disconnect": self.disconnect_button["state"],
                "capture": self.capture_button["state"],
                "group": self.group_button["state"],
                "extract": self.extraer_button["state"],
                "predict": self.predecir_button["state"],
                "train": self.train_button["state"],
                "exit": self.exit_button["state"],
                "change": self.change_button["state"],
            }
        
            self.connect_button["state"] = tk.NORMAL
            self.disconnect_button["state"] = tk.NORMAL
            self.capture_button["state"] = tk.NORMAL
            self.group_button["state"] = tk.NORMAL
            self.extraer_button["state"] = tk.NORMAL
            self.predecir_button["state"] = tk.NORMAL
            self.train_button["state"] = tk.NORMAL
            self.exit_button["state"] = tk.NORMAL
            self.change_button["state"] = tk.NORMAL
        else:
            
            self.connect_button["state"] = self.last_button_state["connect"]
            self.disconnect_button["state"] = self.last_button_state["disconnect"]
            self.capture_button["state"] = self.last_button_state["capture"]
            self.group_button["state"] = self.last_button_state["group"]
            self.extraer_button["state"] = self.last_button_state["extract"]
            self.predecir_button["state"] = self.last_button_state["predict"]
            self.train_button["state"] = self.last_button_state["train"]
            self.exit_button["state"] = self.last_button_state["exit"]
            self.change_button["state"] = self.last_button_state["change"]
            

    def load_files(self, directorio):
        lista_ficheros = []
        for directorio_actual, _, archivos in os.walk(directorio):
            for f in archivos:
                if f.endswith(".json"):
                    lista_ficheros.append(os.path.join(directorio_actual, f))
        return lista_ficheros

    def on_closing(self):
        self.root.destroy()
        
def crear_directorios():
    # Lista de nombres de directorios a crear
    directorios = ["positivo1", "positivo2", "positivo3", "positivo4", "positivo5", "positivo6",
                   "negativo1", "negativo2", "negativo3", "negativo4", "negativo5", "negativo6",
                   "prediccion"]

    # Ruta del directorio principal
    directorio_principal = "./casos"  # Reemplaza esto con la ruta deseada

    # Crear los directorios si no existen
    for directorio in directorios:
        ruta_directorio = os.path.join(directorio_principal, directorio)
        if not os.path.exists(ruta_directorio):
            os.makedirs(ruta_directorio)
            print(f"Directorio '{directorio}' creado en '{directorio_principal}'")
        else: print("Ls directorios ya existen")
        
def erase_file(filename):
    with open(filename, 'w') as archivo:
        # Sobrescribe el contenido con una cadena vacía
        archivo.write('')


if __name__ == "__main__":
    root = tk.Tk()
    vrep_manager = VrepManager()
    app = InterfazGrafica(root, vrep_manager)
    root.mainloop()
