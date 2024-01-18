import funciones as fn
import json
FILE_CCAA = "../entradasUTF8/comunidadAutonoma-Provincia.htm"
DATA = "../entradasUTF8/poblacionProvinciasHM2010-17.csv"
OUTFILE = "intermedio.csv"

prov = fn.read_provincia(FILE_CCAA)
fn.formatInput(DATA, "Total Nacional", "Notas", OUTFILE)
info,years = fn.read_input_to_data_array(OUTFILE)
data = fn.format_info_dict(info,years)
arr = fn.getdata_per_ccaa(prov, data)
rango = fn.get_most_populated(arr)
fn.draw_bar(rango, 10)