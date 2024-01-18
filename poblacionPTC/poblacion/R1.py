import funciones as fn
import funcionesOptimizada as fnOPT
FILE = "../entradasUTF8/poblacionProvinciasHM2010-17.csv"
OUTFILE = "intermedio.csv"

# fn.formatInput(FILE, "Total Nacional", "Notas", OUTFILE)
# tableAbs, tableRel, head, provincias  = fn.getVariaciones(OUTFILE,7)  
# # tableAbs, tableRel, head, provincias  = fn.getVariaciones_subconjunto_de_anios(OUTFILE,0,4)  

# html = fn.generateHTMLR1(tableAbs,tableRel, head[:-1],provincias)
# print(html)

######################################################################################
######################################################################################

fn.formatInput(FILE, "Total Nacional", "Notas", OUTFILE)
# tableAbs, tableRel, head, provincias  = fn.getVariaciones(OUTFILE,7)
# html = fn.generateHTMLR1(tableAbs,tableRel, head[:-1],provincias)
# print(html)
tableAbs, tableRel, head, provincias  = fn.getVariaciones_subconjunto_de_anios(OUTFILE,0,8)
html = fn.generateHTMLR1(tableAbs,tableRel, head[:-1],provincias)
print(html)