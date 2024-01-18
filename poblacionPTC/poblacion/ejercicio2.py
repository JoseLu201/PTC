import csv
import numpy as np
import bs4

import funciones as fn

FILE = "../entradasUTF8/comunidadesAutonomasBis.htm"
FILE_CCAA = "../entradasUTF8/comunidadAutonoma-Provincia.htm"


def read_CCAA(file):
    ficheroInicial=open(file, encoding="utf8")

    soup = bs4.BeautifulSoup(ficheroInicial.read(), 'html.parser')

    # Encontrar la tabla en el documento
    table = soup.find('table', {'class': 'miTabla'})
    rows = table.find_all('tr')

    # Iterar a través de las filas y extraer las parejas de código y nombre
    ccaa = []
    for row in rows[1:]:  # Ignorar la primera fila de encabezado
        cells = row.find_all('td')
        if len(cells) == 2:
            codigo = cells[0].text.strip()
            nombre = cells[1].text.strip()
            ccaa.append((codigo,nombre))
            
    ccaa = np.array(ccaa)
    # print(ccaa)
    return ccaa

def read_provincia(file):
    ficheroInicial=open(file, encoding="utf8")

    soup = bs4.BeautifulSoup(ficheroInicial.read(), 'html.parser')

    # Encontrar la tabla en el documento
    table = soup.find('table', {'class': 'miTabla'})
    
    rows = table.find_all('tr')
    # Iterar a través de las filas y extraer las parejas de código y nombre
    ccaa = {}
    for row in rows[1:]:  # Ignorar la primera fila de encabezado
        cells = row.find_all('td')
        # print(cells)
        if len(cells) == 4:
            codigo = f"{cells[0].text.strip()} {cells[1].text.strip()}" 
            prov = f"{cells[2].text.strip()} {cells[3].text.strip()}"
            if codigo in ccaa:
                ccaa[codigo].append(prov)
            else:
                ccaa[codigo] = [prov]
    # for key, value in ccaa.items():
    #     print(f"{key}: {value}")
    return ccaa

prov = read_provincia(FILE_CCAA)

DATA = "../entradasUTF8/poblacionProvinciasHM2010-17.csv"
OUTFILE = "intermedio.csv"
fn.formatInput(DATA, "Total Nacional", "Notas", OUTFILE)
    

# with open(OUTFILE, encoding="utf8") as csvarchivo:
#         poblacionDict = csv.DictReader(csvarchivo, delimiter=';')
#         next(poblacionDict) 
#         print(poblacionDict.fieldnames)
#         years = poblacionDict.fieldnames[1:-1]
#         years_separados = np.array_split(years,3)
#         print(years_separados)
#         final = {}
        
#         for ccaa,provincias in prov.items():
#             print("\t",ccaa)
#             print("\t",provincias)
#             suma_por_ccaa = {}

#             for d in poblacionDict:
#                 if(d['Provincia'] in provincias):
#                     for y in years_separados[0]:
#                         if y in suma_por_ccaa:
#                             suma_por_ccaa[y].append(d[y])
#                         else:
#                             suma_por_ccaa[y] = [d[y]]
#             poblacionDict.restval
#             final[ccaa] = suma_por_ccaa


# Crear una lista para almacenar los datos del archivo CSV
data = []
final = {}
with open(OUTFILE, encoding="utf8") as csvarchivo:
    poblacionDict = csv.DictReader(csvarchivo, delimiter=';')
    next(poblacionDict)
    years = poblacionDict.fieldnames[1:-1]
    years_separados = np.array_split(years,3)
    
    # Leer los datos del archivo CSV y almacenarlos en la lista "data"
    for row in poblacionDict:
        data.append(row)
        

# Ahora puedes iterar sobre la lista "data" múltiples veces sin problemas
for ccaa, provincias in prov.items():
    # print("\t", ccaa)
    # print("\t", provincias)
    suma_por_ccaa = {}

    for d in data:
        if d['Provincia'] in provincias:
            for y in years:
                if y in suma_por_ccaa:
                    suma_por_ccaa[y].append(d[y])
                else:
                    suma_por_ccaa[y] = [d[y]]
    
    final[ccaa] = suma_por_ccaa

    
            
# for key, value in final.items():
#         print(f"{key}: ")
#         for sub_key, v in value.items():
#             print(f"\t{sub_key:}: {v}")
            
# for key, value in final.items():
#         print(f"{key}: ")
#         for sub_key, v in value.items():
#             print(f"\t{sub_key:}: {np.sum(float(ele) for ele in v)}")
            # print(f"\t{sub_key:}: {v}")

                    
def generateHTML2(data, headers):
    html_table = '''<!DOCTYPE html><html><head><title>Ejemplo tabla</title>
<link rel="stylesheet" href="estilo.css"> <meta charset="utf8"></head>
<body>'''

    first_row = f'''<tr>
            <th rowspan="2">CCAA</th>
            <th colspan="{len(headers)/3}">Total</th>
            <th colspan="{len(headers)/3}">Hombre</th>
            <th colspan="{len(headers)/3}">Mujere</th>
        </tr>
        '''
    

    html_table += "<table>"
    html_table += first_row
    html_table += '''<tr>'''  # Add the header row
    # print(headers)
    # headers.extend([e for e in headers[1:]])
    for header in headers:
        html_table += f"<th>{header}</th>"
    html_table += "</tr>"  # Close the header row

    # Iterate through the matrix and add rows and cells to the table    
    for key, value in data.items():
        html_table += "<tr>"
        html_table += f"<td>{key}</td>"
        for sub_key, v in value.items():
            sum = np.sum(float(ele) for ele in v)
            html_table += f"<td>{sum:.0f}</td>"
        html_table += "</tr>"

    # Close the table
    html_table += "</table></body></html>"
    return html_table


# print(generateHTML2(final, years))

#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

def get_most_populated(final):
    mediasDic = {}
    for key, value in final.items():
        # print(f"{key}: ")
        arr = np.array([]);
        for sub_key, v in value.items():
            if('T' in sub_key):
                suma = np.sum([float(ele) for ele in v])
                arr = np.append(arr, suma)
                # print(f"\t{sub_key:}: {suma}")
                # print(f"\t{sub_key:}: {v}")
        mediasDic[key] = arr   
    return mediasDic

import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8') 
mediasDic = get_most_populated(final)


final_final = {}
for key, val in mediasDic.items():
    
    suma = np.mean(val)
    formatted_value = locale.format_string("%f", suma, grouping=True)
    # print(f"{key:40} : {formatted_value:10}")
    final_final[key] = suma
    
for key, value in final_final.items():
    print(f"{key:40} : {value} ")
 
sorted_pairs = (sorted(final_final.items(), key=lambda item: item[1], reverse=True))
# Print the sorted data
most_populated = np.array([])
for pair in sorted_pairs[:10]:
    formatted_value = locale.format_string("%f", pair[1], grouping=True)
    # print(f"{pair[0]} : {formatted_value}")
    most_populated = np.append(most_populated, pair[0])
    

grafica = {}
genero = {}
sum_por_anios_hombre = np.array([])
sum_por_anios_mujer = np.array([])

for ccaa in most_populated:
    for key, value in final.items():
        if key in ccaa:
            # print(f"->{key}")
            for anio, v in value.items():
                if 'H' in anio:
                    # print(f"\t{anio} : {v}")
                    sum_por_anios_hombre = np.append(sum_por_anios_hombre, np.sum(float(ele) for ele in v))
                if 'M' in anio:
                    # print(f"\t{anio} : {v}")
                    sum_por_anios_mujer = np.append(sum_por_anios_mujer, np.sum(float(ele) for ele in v))
            
            genero['H'] = np.mean(sum_por_anios_hombre)
            genero['M'] = np.mean(sum_por_anios_mujer)
            
                
            grafica[key] = dict(genero)


# for key, values in grafica.items():
#     print(f"{key}")
#     for sub_key, v in values.items():
#         print(f"\t{sub_key} : {v}")
                    
import matplotlib.pyplot as plt
def draw_bar(grafica):
    # Extraer las comunidades, hombres y mujeres de los datos
    communities = list(grafica.keys())
    men_values = [entry['H'] for entry in grafica.values()]
    women_values = [entry['M'] for entry in grafica.values()]

    x = np.arange(len(communities))

    # Ancho de las barras
    bar_width = 0.35

    # Crear el gráfico de barras
    plt.bar(x - bar_width/2, men_values, bar_width, label='Hombres', color='blue')
    plt.bar(x + bar_width/2, women_values, bar_width, label='Mujeres', color='red')

    # Etiquetas de las comunidades
    plt.xticks(x, communities, rotation=90)
    # Ajustar el tamaño del texto de los ejes y moverlo a la izquierda
    plt.tick_params(axis='x', labelsize=8, pad=0, )
    

    # Agregar etiquetas
    plt.xlabel('Comunidades Autónomas')
    plt.ylabel('Media')
    plt.title('Poblacion por sexo en el año 2017 (CCAA)')
    plt.legend()

    # Mostrar el gráfico
    plt.tight_layout()
    # plt.show()
    
# draw_bar(grafica)
                    


