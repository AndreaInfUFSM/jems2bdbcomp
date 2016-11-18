#!/usr/bin/python3

# Cadastra artigos na BDBCOMP a partir de dados em CSV obtidos do JEMS
# ANTES de usar este script:
# 1) Cadastre o evento manualmente na BDBCOMP
# 2) Substitua os dados do evento no script
#    - use os mesmos dados informados no cadastro do evento
#    - veja abaixo como obter a sigla da conferencia na BDBCOMP
# 3) Escolha as linhas do CSV a cadastrar
#
# Author: andrea@inf.ufsm.br
#

from lxml import etree, html
import csv
import io
import urllib.request
import requests
import sys


# --- Altere configuracoes abaixo ---

# A sigla da conferencia é interna à BDBCOMP e pode ser obtida olhando o código fonte
# da página http://www.lbd.dcc.ufmg.br/curadoria/inserir_artigo_evento.php,
# próximo a 'Selecione o Evento no qual deseja inserir Artigos'
conference = 'erad-rj' # sigla da conferencia na BDBCOMP
# Os dados abaixo devem ser identicos aos informados no cadastro do evento
year = '2015'   # ano da conferencia
vol = 'I'       # edicao da conferencia
quant = '9'     # quantidade de artigos
lang = 'por'    # idioma: português

example1 = 'https://docs.google.com/spreadsheets/d/1DZobJuA-XdWP7ltQbmRUVQByuxOc_GWhn81cjKzvo8c/pub?output=csv'
example2 = 'output.csv'

# A entrada pode ser um arquivo local ou uma planilha publicada no Google Drive
inputname = example2

# Linhas do CSV a processar (numeradas a partir de 1, que é o cabeçalho)
rangestart = 2  # primeira linha a cadastrar
rangeend = 3    # ultima linha, nao incluida no cadastro
# ---------------------------------------


bdburl = 'http://www.lbd.dcc.ufmg.br/curadoria/inserir_artigo_evento.php'

def newDataParam(row):

    # Campos estao na ordem em que foram capturados na requisicao
    data = {
        'titulo' : row[0],
        'autor[]': row[1].split(','),
        'idioma' : lang,
        'resumo' : row[2],
        'pagina_inicial': row[4] if len(row) > 4 else '',
        'pagina_final': row[5] if len(row) > 5 else '',
        'sigla': conference,
        'ano': year,
        'volume': vol,
        'pdfs':"1",
        'quantidade_artigos': quant,
        'salvar':"Salvar"
    }
    return data

def newFilesParam(row):
    files = {'arquivo': (row[3], open(row[3], 'rb'), 'application/pdf')}
    return files

def parseResponse(htmltext):
    myparser = etree.HTMLParser(encoding="utf-8")
    tree = etree.HTML(htmltext, parser=myparser)
    success = tree.xpath('//fieldset/ul/li')
    if len(success) > 0:
        print('Success:', success[0].xpath('b/text()')[0])

def bdbinsert(row):
    payload = newDataParam(row)
    files = newFilesParam(row)
    r = requests.post(bdburl, data=payload, files=files)
    #print(r.text)
    parseResponse(r.text)

# Poor-man's URL checker
def isHttp(name):
    return name[0:4] == 'http'

def getRange(argv):
    if len(argv) == 1:
        selectedrows = range(rangestart, rangeend) # starting from 1, not 0
    elif len(argv) == 2:
        selectedrows = range(int(argv[1]), int(argv[1])+1)
    elif len(argv) > 2:
        selectedrows = range(int(argv[1]), int(argv[2]))
    return selectedrows


def main(argv):

    selectedrows = getRange(argv)
    csvfile = urllib.request.urlopen(inputname) if isHttp(inputname) else open(inputname, "rb")
    with csvfile:
        reader = csv.reader(io.TextIOWrapper(csvfile),
            delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for i, row in enumerate(reader):
            if i+1 in selectedrows:
                bdbinsert(row)


if __name__ == "__main__":
    main(sys.argv)
