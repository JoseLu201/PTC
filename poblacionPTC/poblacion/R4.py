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
dictVarAbs, dictVarRel = fn.calculosR4(arr)
# fn.printDict(dictVarAbs)
# fn.printDict(dictVarRel)

# print(dictVarAbs[(next(iter(dictVarAbs)))].keys())
text = fn.generateHTMLR4(dictVarAbs, dictVarRel)
# print(text)

            
