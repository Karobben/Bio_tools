#!/usr/bin/env python3.7
import argparse

#命令行输入参数处理
parser = argparse.ArgumentParser()
parser.add_argument('-i','-I','--input')     #输入文件
parser.add_argument('-o','-O', '--output',default = "out.table")   #输出文件

#获取参数
args = parser.parse_args()

FILE = args.input
OUTPUT = args.output


####grep information from uniprot
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import re
import pandas as pd

import multiprocessing as mp
import time


def print_result(INPUT,Infor):
    for i in Infor:
        if INPUT in i.get_text().split('\n')[0]:
            return i.get_text().split('\n')[1]

sit="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc="
#list = pd.read_csv(FILE,header=None)

list=''
f = open(FILE, "r")
list +=f.read() +' '
list=list.split("\n")

i = list[0]
def NCBI_grep(i):
    url = sit + i
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    Infor = soup.find_all('tr', {'valign':'top'})
    #GSM ID, Title, Charaacteristics ...
    Sample_r = Infor[0].get_text().split('\n')[0].replace('Sample ','')
    Title_r = print_result('Title',Infor)
    Cha = print_result('Characteristics',Infor).replace('gender','\nGender').replace('smoking','\nsmoking').replace('Stage','\nStage').split('\n')
    Platform_ID = print_result('Platform ID',Infor)
    Series_1 = print_result('Series (1)',Infor)
    SRA_r = print_result('SRA',Infor)
    BioSample_r = print_result('BioSample',Infor)
    return [Sample_r,Title_r,Cha[0],Cha[1],Cha[2],Cha[3],Platform_ID,Series_1,SRA_r,BioSample_r]

TB = NCBI_grep(i)
TB = pd.DataFrame(TB)
for i in list[1:-1]:
    TB2 = NCBI_grep(i)
    TB2 = pd.DataFrame(TB2)
    TB= pd.concat([TB, TB2], axis=1, sort=False)

TB.to_csv(OUTPUT,sep='\t',quoting=None,header=None, index=None)
