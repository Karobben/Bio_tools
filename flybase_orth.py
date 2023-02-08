#!/usr/bin/env python3
import argparse
import multiprocessing as mp
#命令行输入参数处理
parser = argparse.ArgumentParser()
parser.add_argument('-i','-I','--input', nargs='+')     #输入文件
parser.add_argument('-p','-P','--process', type = int, default = 10)     #输入文件

args = parser.parse_args()

ID = args.input
Pool = args.process

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

def Run(ID):
    url = "https://api.flybase.org/api/v1.0/chadoxml/" + ID
    html = urlopen(url)
    soup = BeautifulSoup(html, features='xml')

    Orth_all = [i for i in  soup.find_all("feature_relationship") if i.find('name').get_text() == 'orthologous_to']
    Orth_Homo = [i  for i in Orth_all if i.find('genus').get_text() == 'Homo']
    Gene_Syambol = [i.find_all('name')[2].get_text().split('\\')[1] for i in Orth_Homo]
    Gene_Ensembl = {}

    for ii in Orth_Homo:
        for i in ii.find_all("dbxref_id"):
            if i.find('name').get_text() == "Ensembl_Homo_sapiens":
                Gene_Ensembl.update({ii.find_all('name')[2].get_text().split('\\')[1]:i.find('accession').get_text()})

    TB = pd.DataFrame(Gene_Ensembl,  index=[1]).T
    TB['ID'] = ID
    print(TB)
    return TB

def multicore(Pool=Pool):
  pool = mp.Pool(processes=Pool)
  for i in ID:
    # Working function "echo" and the arg 'i'
    multi_res = [pool.apply_async(Run,(i,))]
  pool.close()
  pool.join()

multicore()
