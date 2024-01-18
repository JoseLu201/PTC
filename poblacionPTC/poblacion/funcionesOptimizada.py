import csv
import numpy as np
import matplotlib.pyplot as plt
import funciones as fn
FILE = "../entradasUTF8/poblacionProvinciasHM2010-17.csv"
OUTFILE = "intermedio.csv"

# Dato un fichero corta la cadena entre dos string y lo guarda en otro archivo
# Cabecera?!?!!?!?
def formatInput(file, init_string, end_string, outfile):
    with open(file, encoding="utf8") as ficheroInicial:
        cadenaPob = ficheroInicial.read()
        primero = cadenaPob.find(init_string)
        ultimo = cadenaPob.find(end_string)
        cadenaFinal = cadenaPob[primero:ultimo]
        cabecera = "Provincia;T2017;T2016;T2015;T2014;T2013;T2012;T2011;T2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011;H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010;"
        cadenaFinal = cabecera + '\n' + cadenaFinal
        with open(outfile, "w", encoding="utf8") as ficheroFinal:
            ficheroFinal.write(cadenaFinal)
    
# formatInput(FILE, "Total Nacional", "Notas", OUTFILE)

# Dado un input en notacion cientifica lo convertimos a una string en formato float
def format_scientic(inp):
    parts = inp.split('E')
    integer_part, exponent = float(parts[0]), int(parts[1])
    #print(str(int(integer_part * 10 ** exponent)) + '0'*exponent)
    return str(int(integer_part * 10 ** exponent)) 

# np.set_printoptions(suppress=True, formatter={'float_kind':'{:.2f}'.format})

# Una vez leidos los datos del archivo y un conjunto de años, calcular las variaciones
def getVariaciones(file,num_year):
    with open(file, encoding="utf8") as csvarchivo:
        poblacionDict = csv.DictReader(csvarchivo, delimiter=';')
        
        tableAbs = []
        tableRel = []
        provincias = []
        
        years = poblacionDict.fieldnames[1:num_year+2]

        for regD in poblacionDict:
            arrAbs = [float(regD[years[i]]) - float(regD[years[i+1]]) for i in range(len(years) - 1)]
            arrRel = [((diff / float(last)) * 100) for diff, last in zip(arrAbs, regD[years[1]:])]
            
            tableAbs.append(arrAbs)
            tableRel.append(arrRel)
            provincias.append(regD['Provincia'])
            
        return tableAbs, tableRel, years, provincias

'''
First Year es el indice del primer año del cual queremos partir, por ejemplo 2017
Last Year es el ultimo indice, por ejemplo 4 -> 2013 por lo que la informacion que obtendremos sera entre 2017 y 2013+1
'''
def getVariaciones_subconjunto_de_anios(file,first_year,last_year):
    tableAbs, tableRel, head, provincias  = fn.getVariaciones(file,7)
    head_n = []
    head_n.append(head[0])
    head_n.extend(head[first_year+1:last_year])
    tableAbs = tableAbs[:,first_year:last_year-1]
    tableRel = tableRel[:,first_year:last_year-1]
    return tableAbs, tableRel, head_n, provincias 

def generateHTMLTable(data, headers):
    html_table = '''<!DOCTYPE html><html><head><title>Ejemplo tabla</title>
<link rel="stylesheet" href="estilo.css"> <meta charset="utf8"></head>
<body>'''

    # Construir la tabla de encabezado
    html_table += "<table>"
    html_table += "<tr>"  # Agregar la fila de encabezado
    for header in headers:
        html_table += f"<th>{header}</th>"
    html_table += "</tr>"  # Cerrar la fila de encabezado

    # Iterar a través de los datos y agregar filas y celdas a la tabla    
    for key, values in data.items():
        html_table += "<tr>"
        html_table += f"<td>{key}</td>"
        for value in values:
            html_table += f"<td>{value:.2f}</td>"
        html_table += "</tr>"

    # Cerrar la tabla
    html_table += "</table></body></html>"
    return html_table



def generateHTMLR1(tableAbs,tableRel, headers, provincias):
    html_table = '''<!DOCTYPE html><html><head><title>Ejemplo tabla</title>
<link rel="stylesheet" href="estilo.css"> <meta charset="utf8"></head>
<body>'''

    first_row = f'''<tr>
            <th></th>
            <th colspan="{len(headers)-1}">Variacion Absoluta</th>
            <th colspan="{len(headers)-1}">Variacion Relativa</th>
        </tr>'''
    

    html_table += "<table>"
    html_table += first_row
    html_table += "<tr>"  # Add the header row

    headers.extend([e for e in headers[1:]])
    for header in headers:
        html_table += f"<th>{header}</th>"
    html_table += "</tr>"  # Close the header row

    # Iterate through the matrix and add rows and cells to the table    
    for prov,abs,rel in zip(provincias,tableAbs, tableRel):
        html_table += "<tr>"
        html_table += f"<td>{prov}</td>"
        for cell in abs:
            html_table += f"<td>{cell:.2f}</td>"
            
        for cell in rel:
            html_table += f"<td>{cell:.2f}</td>"
        html_table += "</tr>"

    # Close the table
    html_table += "</table></body></html>"
    return html_table
    

# tableAbs, tableRel, head, provincias  = getVariaciones(OUTFILE,7)  
# tableAbs, tableRel, head, provincias  = getVariaciones_subconjunto_de_anios(OUTFILE,0,4)  

# html = generateHTML2(tableAbs,tableRel, head[:-1],provincias)
# print(html)
         
######################################################################
######################################################################
######################################################################

FILE_R2 = "../entradasUTF8/comunidadesAutonomasBis.htm"
FILE_CCAA = "../entradasUTF8/comunidadAutonoma-Provincia.htm"

import bs4  


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
formatInput(DATA, "Total Nacional", "Notas", OUTFILE)



def read_input_to_data_array(file):
    data = []
    with open(file, encoding="utf8") as csvarchivo:
        poblacionDict = csv.DictReader(csvarchivo, delimiter=';')
        # print(poblacionDict.fieldnames)
        years = poblacionDict.fieldnames[1:-1]
        # years_separados = np.array_split(years,3)
        
        # Leer los datos del archivo CSV y almacenarlos en la lista "data"
        for row in poblacionDict:
            data.append(row)
    return data,years

# info,years = read_input_to_data_array(OUTFILE)

def format_info_dict(info, years):
    data = {}
    for entry in info:
        anios_t = dict()
        prov = entry['Provincia'] 
        for y in years:
            anios_t[y] = entry[y]
        data[entry['Provincia']] = anios_t
    return data
        

# data = format_info_dict(info,years)

import json
# datos_poblacion_json = json.dumps(data, indent=4)

# print(datos_poblacion_json)

def getdata_per_ccaa(provincias, datos):
    final = {}
    for ccaa, provincias in prov.items():
        suma_por_ccaa = dict()
        for nombre_provincia,values in datos.items():
            if nombre_provincia in provincias:
                for anios, pobl in values.items():
                    if anios in (suma_por_ccaa):
                        suma_por_ccaa[anios].append(pobl)
                    else:
                        suma_por_ccaa[anios] = [pobl]

        final[ccaa] = suma_por_ccaa
    return final


# arr = getdata_per_ccaa(prov, data)
# datos_final_json = json.dumps(final, indent=4)
# print(datos_final_json)


def calcular_poblacion_por_ccaa(datos):
    final = dict()
    
    for prov, pobl in datos.items():
        suma = dict()
        for anio, valor in pobl.items():
            suma[anio] = np.sum(float(ele) for ele in valor)
        final[prov] = suma
    return final

    
# print(final['01 Andalucía'])
# muestra = calcular_poblacion_por_ccaa(arr)
# print((muestra[(next(iter(muestra)))].keys()))
# datos_final_json = json.dumps(muestra, indent=4)
# print(datos_final_json)
    
def generateHTMLR2(data):
    html_table = '''<!DOCTYPE html><html><head><title>Ejemplo tabla</title>
<link rel="stylesheet" href="estilo.css"> <meta charset="utf8"></head>
<body>'''
    headers = data[(next(iter(data)))]
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
    for header in headers.keys():
        html_table += f"<th>{header}</th>"
    html_table += "</tr>"  # Close the header row

    # Iterate through the matrix and add rows and cells to the table    
    for key, value in data.items():
        # print(f"{key} : {value}")
        html_table += "<tr>"
        html_table += f"<td>{key}</td>"
        for sub_key, v in value.items():
            # print(f"{sub_key} : {v}")
            
            # sum = np.sum(float(ele) for ele in v)
            html_table += f"<td>{v:.0f}</td>"
        html_table += "</tr>"

    # Close the table
    html_table += "</table></body></html>"
    return html_table

def printDict(dic):
    for key, value in dic.items():
        print(f"{key}: ")
        for sub_key, v in value.items():
            print(f"\t{sub_key} : {v}")
            
#######################################################
def get_most_populated(datos):
    mediasDic = {}
    for key, value in datos.items():
        # print(f"{key}: ")
        arr = np.array([])
        arr_h = np.array([])
        arr_m = np.array([])
        
        for sub_key, v in value.items():
            if('T' in sub_key):
                suma = np.sum([float(ele) for ele in v])
                arr = np.append(arr, suma)
            if('H' in sub_key):
                suma = np.sum([float(ele) for ele in v])
                arr_h = np.append(arr_h, suma)
            if('M' in sub_key):
                suma = np.sum([float(ele) for ele in v])
                arr_m = np.append(arr_m, suma)
        # mediasDic[key] = arr 
        
        mediasDic[key] =  {'T':np.mean(arr),
                          'H':np.mean(arr_h),   
                          'M':np.mean(arr_m)}   
        
    #Ordenamos segun el total 'T' de mayor a menor (reverse)    
    return  dict(sorted(mediasDic.items(), key=lambda item: item[1]['T'], reverse=True))
    
def draw_bar(datos):
    # Extraer las comunidades, hombres y mujeres de los datos
    communities = list(datos.keys())
    men_values = [entry['H'] for entry in datos.values()]
    women_values = [entry['M'] for entry in datos.values()]

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
    plt.show()
    
def calculate_category_variations(years, values):
    sub_dict_abs = {}
    sub_dict_rel = {}
    for i in range(len(years) - 1):
        actual_population = values[years[i]]
        previous_population = values[years[i + 1]]      
        variation_abs = actual_population - previous_population
        variation_rel = (variation_abs / previous_population) * 100
        sub_dict_abs[years[i]] = variation_abs
        sub_dict_rel[years[i]] = variation_rel
    return sub_dict_abs, sub_dict_rel

def calculosR4(datos):
    for key, value in datos.items():
            datos[key] = {}
            for sub_key, v in value.items():
                datos[key][sub_key] = np.sum([float(ele) for ele in v])

    dictVarAbs = {}
    dictVarRel = {}
    for ccaa, value in datos.items():
        years = [y for y in value.keys() if 'T' not in y]
        years_h = years[:len(years)//2]
        years_m = years[len(years)//2:]
        # print(years_h, years_f)
        
        sub_dict_abs, sub_dict_rel = calculate_category_variations(years_h, value)
        sub_dict_abs2, sub_dict_rel2 = calculate_category_variations(years_m, value)

        for key, value in sub_dict_abs2.items():
            if key in sub_dict_abs:
                sub_dict_abs[key] += value
            else:
                sub_dict_abs[key] = value

        for key, value in sub_dict_rel2.items():
            if key in sub_dict_rel:
                sub_dict_rel[key] += value
            else:
                sub_dict_rel[key] = value
                
        dictVarAbs[ccaa] = sub_dict_abs
        dictVarRel[ccaa] = sub_dict_rel
    return dictVarAbs, dictVarRel


def generateHTMLR4(dataAbs,dataRel):
    html_table = '''<!DOCTYPE html><html><head><title>Ejemplo tabla</title>
<link rel="stylesheet" href="estilo.css"> <meta charset="utf8"></head>
<body>'''
    headers = dataAbs[(next(iter(dataAbs)))]
    wide = 6
    first_row = f'''
            <tr>
                <th colspan="{wide}"></th>    
                <th colspan="{len(headers)}">Variacion Total</th>
                <th colspan="{len(headers)}">Variacion Relativa</th>
            </tr>
            <tr>
                <th colspan="{wide}"    ></th>
                <th colspan="{len(headers)/2}">Hombre</th>
                <th colspan="{len(headers)/2}">Mujere</th>
                <th colspan="{len(headers)/2}">Hombre</th>
                <th colspan="{len(headers)/2}">Mujere</th>
            </tr>
        '''
    

    html_table += "<table>"
    html_table += first_row
    html_table += '''<tr>'''  # Add the header row
    cabecera = ''''''
    for header in headers.keys():
        cabecera += f"<th>{header}</th>"
    cabecera = 2*cabecera
    cabecera = f'''<th colspan="{wide}"></th>''' + cabecera
    html_table += cabecera
    html_table += "</tr>"  # Close the header row

    # Iterate through the matrix and add rows and cells to the table    
    for (key1, value1), (key2, value2) in zip(dataAbs.items(), dataRel.items()):
        # print(f"{key} : {value}")
        html_table += "<tr>"
        html_table += f"<td colspan=\"{wide}\">{key1}</td>"
        for sub_key, v in value1.items():
            html_table += f"<td>{v:.0f}</td>"
        for sub_key, v2 in value2.items():
            html_table += f"<td>{v2:.2f}</td>"
        html_table += "</tr>"

    # Close the table
    html_table += "</table></body></html>"
    return html_table

# Le pasamos las comunidades ordenadas (ccaa)
# y la informacion de cada una de ellas
def getCCAA_Population_per_Years(ccaa, data):
    poblacionTotal = {}
    for key, _ in ccaa.items():
        anio_population = {}
        for sub_key, values in data[key].items():
            if 'T' in sub_key:
                anio_population[sub_key] = np.sum(float(ele) for ele in values)
        poblacionTotal[key] = anio_population;
    return poblacionTotal
    

def printGraphR5(poblacionTotal, n_ccaa):
   
    comunidades = list(poblacionTotal.keys())[:n_ccaa]
    años = list((poblacionTotal[(next(iter(poblacionTotal)))].keys()))
    años.reverse()
    #Primero creo un array sacando los valores de poblacion
    poblaciones = {comunidad: [poblacionTotal[comunidad][año] for año in años] for comunidad in comunidades}
    print(poblaciones)
    fig, ax = plt.subplots(figsize=(10, 6))

    for comunidad in comunidades:
        ax.plot(años, poblaciones[comunidad], marker='o', label=comunidad)

    ax.set_xlabel('Años')
    ax.set_ylabel('Población')
    ax.set_title('Población por Comunidad Autónoma')
    ax.grid(False)  # Quitar el grid

    # Mostrar valores del eje y en notación científica
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

    # Mover la leyenda fuera del gráfico
    ax.legend(loc='upper left')

    plt.show()




