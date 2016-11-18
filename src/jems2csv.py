#!/usr/bin/python3

# Extrai dados de arquivos do JEMS e coloca-os em formato CSV
# Author: andrea@inf.ufsm.br

from lxml import etree
import sys
import csv

# Descompacte em datadir o arquivo obtido em:
# JEMS -> Conference -> Publication chair options -> Download metadata
# Descompacte em absdir o arquivo obtido em:
# JEMS -> Conference -> Chair -> Configurations -> Export all data
datadir = '../data/meta'
datafile = datadir + '/' + 'index.xml'
absdir = '../data/all'
absfile = absdir + '/' + 'papers.xml'


def parseAbstracts(input):
    abdict = {}
    try:
        tree = etree.parse(input)
        papers = tree.xpath('//row')
        for p in papers:
            title = p.xpath("field[contains(@name,'papertitle')]/text()")[0]
            abstract = p.xpath("field[contains(@name,'abstract')]/text()")[0]
            abdict[title] = abstract
    except:
        abdict = {}
    return abdict

def parsePapers(input):
    data = []
    try:
        tree = etree.parse(input)
        papers = tree.xpath('//publ')
        for p in papers:
            title = p.xpath('title/text()')[0]
            authors = p.xpath('author/text()')
            authorstr = ''
            for a in authors:
                authorstr += ',' + a
            pdf = datadir + '/' + p.xpath('ee/text()')[0][1:]
            data.append(dict(title=title, authors=authorstr[1:], pdf=pdf))
    except:
        data = []
    return data


def main():
    abdict = parseAbstracts(absfile)
    data = parsePapers(datafile)
    w = csv.writer(sys.stdout, delimiter=',', quotechar='"')
    w.writerow(['title','authors','abstract','pdf'])
    for p in data:
        # Talvez reescrever este codigo com um ordered dictionary?
        w.writerow([
            p['title'],
            p['authors'],
            abdict.get(p['title']) or '',
            p['pdf']])


if __name__ == "__main__":
    main()
