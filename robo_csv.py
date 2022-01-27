from collections import defaultdict
from pathlib import Path
import re
import os
from numpy import append
import pandas as pd
import gerar_relatorio

def multiplas_trocas(d, text):
    regex = re.compile(r"(%s)" % "|".join(map(re.escape, d.keys())), re.IGNORECASE)
    return regex.sub(lambda mo: d[mo.string[mo.start():mo.end()]], texto)


cEspeciais = {
'á': 'A',
'Â': 'A',
'â': 'A',
'Á': 'A',
'ã': 'A',
'Ã': 'A',
'É': 'E',
'é': 'É',
'ç': 'C',
'Ç': 'C',
'õ': 'O',
'Õ': 'O',
'ó': 'O',
'Ó': 'O',
'Ô': 'O',
'ô': 'O',
';': '',
'<': '',
'>': '',
'\\': '',
'//': '',
'/': '',
'-': '',
'_': '',
'!': '',
'#': '',
'$': '',
'%': '',
'¨': '',
'&': '',
'*': '',
'(': '',
')': '',
'+': '',
'=': '',
'{': '',
'}': '',
'^': '',
'~': '',
'[': '',
']': '',
'?': '',
':': '',
'¹': '',
'²': '',
'³': '',
'£': '',
'¢': '',
'¬': '',
'ª': '',
'º': '',
'°': ''}

subarquivos = [sub for sub in Path(".").glob("**/*.txt")]

relatorio = []
relatorioCsv = []

for subarquivo in subarquivos:
    
    nomeArquivo = str(subarquivo.name)
    original = open(subarquivo, 'r', encoding='latin1')
    rel_exp = re.compile(r'[\sa-zA-Z0-9-.]+')
    lista = rel_exp.finditer(str(original.readline()))
    
    particionado = []
    
    for itens in lista:
        particionado.append(itens)
            
    if particionado[0].group() == '0000': 

        dataInicio = particionado[3].group() 
        dataFim = particionado[4].group() 
        
        inicio = (dataInicio[4]+dataInicio[5]+dataInicio[6]+dataInicio[7]+dataInicio[2]+dataInicio[3]+dataInicio[0]+dataInicio[1])
        fim = (dataFim[4]+dataFim[5]+dataFim[6]+dataFim[7]+dataFim[2]+dataFim[3]+dataFim[0]+dataFim[1])

        print(inicio)
        print(fim)   

        relatorio.append([particionado[6].group(), particionado[5].group(), particionado[7].group(), dataInicio, dataFim])
        relatorioCsv.append([particionado[6].group(), particionado[5].group(), particionado[7].group(), inicio, fim])

        nomeArquivo = re.sub('.txt', '', nomeArquivo)
   
        caminho = str(subarquivo.parent)
        caminhoCompleto = caminho + '\\limpos\\'
        
        
        if not os.path.exists(caminhoCompleto): 
            os.makedirs(caminhoCompleto)
       
        novoTexto = open(caminhoCompleto+subarquivo.name, 'w+', encoding='utf-8')
        original.seek(0)
        texto = original.read()
        resultado = multiplas_trocas(cEspeciais, texto)
        textopronto, lixo, tail = resultado.partition('SBRCAAEPDR0')
       
        novoTexto.write(textopronto)
    
        novoTexto.close()
        original.close()
        
    else:
        pass

relatorioFinal = pd.DataFrame(relatorio)
paraCSV = pd.DataFrame(relatorioCsv)
gerar_relatorio.gerar_relatorio(relatorioFinal)
paraCSV.to_csv(f"relatorio_"+relatorioFinal.loc[0,0]+'.csv', sep=';')