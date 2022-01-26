import datetime
from collections import defaultdict

def gerar_relatorio(lista):
    
    mesesInicial = []
    mesesFinal = []
    relatorio = []

    n = 0
    
    novoTexto = open('relatorio_'+str(lista.loc[0,0])+'.txt', 'w+', encoding='utf-8')
    
    while n < len(lista):

        mesesInicial.append(lista.loc[int(n), 3])
        mesesFinal.append(lista.loc[int(n), 4])
        relatorio.append(f'{lista.loc[int(n), 0]}_{lista.loc[int(n),1]}_{lista.loc[int(n),2]}_{lista.loc[int(n),3]}_{lista.loc[int(n),4]}')
                
        novoTexto.write(str(relatorio[n]))
        novoTexto.write('\n')
        
        n += 1
    

    primeiraData = datetime.datetime.strptime(mesesInicial[0], "%d%m%Y")
    ultimaData = datetime.datetime.strptime(mesesFinal[-1], "%d%m%Y")

    diff = ultimaData - primeiraData
    dias = diff.days
    months, days = dias // 30, dias % 30
    
    if months == len(lista):
        novoTexto.write(f'Relatório com {months} meses e {len(lista)} arquivos:')
        novoTexto.write('\n')
    else:
        novoTexto.write(f'Relatório com incoerências: {months} meses listados e {len(lista)} arquivos apresentados. ')
        novoTexto.write('\n')

    novoTexto.write('Relatorios Duplicados: ')
    novoTexto.write('\n')

    mesesInicial.sort()
    mesesFinal.sort()

    keys = defaultdict(list)
    for key, value in enumerate(mesesInicial):

        keys[value].append(key)

    for value in keys:
        if len(keys[value]) > 1:
            novoTexto.write(str(value))
            novoTexto.write('\n')
    novoTexto.close()
