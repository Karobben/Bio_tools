#!/usr/bin/env python3

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-i','-I','--input', nargs='+')     #输入文件
parser.add_argument('-o','-U','--output', default = "OUT.csv")     #输入文件

##获取参数
args = parser.parse_args()
INPUT = args.input
OUTPUT = args.output

import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen


def Run(ID):
    url = "https://api.flybase.org/api/v1.0/chadoxml/" + ID
    html = urlopen(url)
    soup = BeautifulSoup(html, features='xml')

    Orth_all = [i for i in  soup.find_all("feature_relationship") if i.find('name').get_text() == 'orthologous_to']
    Orth_Homo = [i  for i in Orth_all if i.find('genus').get_text() == 'Homo']
    Gene_Syambol = [i.find_all('name')[2].get_text().split('\\')[1] for i in Orth_Homo]
    #Gene_Ensembl = [[i.find('accession').get_text() for i in ii.find_all("dbxref_id") if i.find('name').get_text() == "Ensembl_Homo_sapiens"][0]  for ii in Orth_Homo]
    Gene_Ensembl = [[i.get_text() for i in ii.find_all('accession') if "ENSG" in i.get_text()] for ii in Orth_Homo]
    TB = pd.DataFrame([Gene_Syambol, Gene_Ensembl]).T
    TB['ID'] = ID
    TB['SAMBOL'] = soup.find_all("name")[5].get_text()
    return TB

TB = pd.DataFrame()
for ID in INPUT:
    print(ID)
    TMP = Run(ID)
    TB =  pd.concat([TB, TMP])


TB.to_csv(OUTPUT)






'''

    for ii in Orth_Homo:
        for i in ii.find_all("dbxref_id"):
            if i.find('name').get_text() == "Ensembl_Homo_sapiens":  
                TMP = [i.find('accession').get_text()]
        Gene_Ensembl += TMP
'''
