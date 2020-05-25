#!/usr/bin/env python3.7
'''
This Script is designed for crawling Uniport ID from websit:
"https://www.kegg.jp/kegg-bin/uniprot_list?ko="
for example: "https://www.kegg.jp/kegg-bin/uniprot_list?ko=K10305"
'''
import argparse

#命令行输入参数处理
parser = argparse.ArgumentParser()
parser.add_argument('-i','-I','--input')     #输入文件
#parser.add_argument('-o','-O', '--output',default = "out.table")   #输出文件

#获取参数
args = parser.parse_args()

ID = args.input
#OUTPUT = args.output


####grep information from uniprot
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import re
import pandas as pd

#import multiprocessing as mp
#import time

sit="https://www.kegg.jp/kegg-bin/uniprot_list?ko=K"

def Kegg2Uniport(i):
    url = sit + i
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    Table = soup.find_all('tr', {'valign':'top'})
    Result = ["\t".join([Table[0].find_all('td')[0].get_text().strip(),Table[0].find_all('td')[1].get_text().strip(),"Name"])]
    for i in Table[1:]:
        line = i.find_all('td')
        Result += ["\t".join([line[0].get_text().strip(),line[1].get_text().strip(),line[3].get_text().strip()])]
    return "\n".join(Result)


print(Kegg2Uniport(ID))
