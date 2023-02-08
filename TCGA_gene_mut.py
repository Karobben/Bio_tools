#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i','-I','--input', nargs='+')
parser.add_argument('-o','-U','--output', default = "Test.csv")
parser.add_argument('-a','-A','--anno', default = False)

args = parser.parse_args()
INPUT = args.input
OUTPUT = args.output
ANNO = args.anno

import json
import requests
import pandas as pd
# require the number of docs have mutation

url = 'https://api.gdc.cancer.gov/analysis/mutated_cases_count_by_project?size=0&pretty=true'
Total = requests.get(url, stream=True)

if Total.json()['timed_out'] == True:
    raise "Error, time out for requests the total counts"

Total = Total.json()['aggregations']['projects']['buckets']
TB_Projects = pd.DataFrame([[i['key'], i['case_summary']['case_with_ssm']['doc_count']] for i in Total], columns=["Projects", 'Counts'])

## Require the mutation counts for each genes

ID = ",".join(INPUT)

url = "https://api.gdc.cancer.gov/analysis/top_cases_counts_by_genes?gene_ids=" + ID
TMP = requests.get(url, stream=True)
if TMP.json()['timed_out'] == True:
    raise "Error, time out for requests the total counts"
TMP = TMP.json()['aggregations']['projects']['buckets']

All = []

for i in TMP:
    Project = i['key']
    for ii in i['genes']['my_genes']['gene_id']['buckets']:
        Genes = ii['key']
        G_count  = ii['doc_count']
        All += [[Project, Genes, G_count]]

Gene_TB = pd.DataFrame(All, columns=["Projects", 'Genes', 'G_Counts'])
Finall_TB = pd.merge(Gene_TB, TB_Projects)

if ANNO != False:
    TB_Anno = pd.read_csv(ANNO, header= None)
    TB_Anno.columns = ['Genes', 'Anno']
    Finall_TB = pd.merge(Finall_TB, TB_Anno)

Finall_TB.to_csv(OUTPUT)


'''
url = "https://api.gdc.cancer.gov/analysis/top_cases_counts_by_genes?value=ssm&gene_ids=" + ID+"&pretty=true&expand=ssms"
TMP = requests.get(url, stream=True)
if TMP.json()['timed_out'] == True:
    raise "Error, time out for requests the total counts"
TMP = TMP.json()['aggregations']['projects']['buckets']

All = []

for i in TMP:
    Project = i['key']
    for ii in i['genes']['my_genes']['gene_id']['buckets']:
        Genes = ii['key']
        G_count  = ii['doc_count']
        All += [[Project, Genes, G_count]]

Gene_TB = pd.DataFrame(All, columns=["Projects", 'Genes', 'G_Counts'])
Finall_TB = pd.merge(Gene_TB, TB_Projects)
Finall_TB[Finall_TB.Projects == "TCGA-READ"]


curl "https://api.gdc.cancer.gov/analysis/top_mutated_cases_by_gene?fields=diagnoses.days_to_death,diagnoses.age_at_diagnosis,diagnoses.vital_status,diagnoses.primary_diagnosis,demographic.gender,demographic.race,demographic.ethnicity,case_id,summary.data_categories.file_count,summary.data_categories.data_category&filters={"op":"and","content":[{"op":"=","content":{"field":"cases.project.project_id","value":"TCGA-DLBC"}},{"op":"in","content":{"field":"genes.gene_id","value":["ENSG00000166710"]}},{"op":"in","content":{"field":"ssms.consequence.transcript.annotation.impact","value":["HIGH"]}}]}&pretty=true&size=2"

curl "https://api.gdc.cancer.gov/analysis/top_mutated_cases_by_gene?fields=diagnoses.days_to_birth,diagnoses.age_at_diagnosis,diagnoses.days_to_birth,diagnoses.primary_diagnosis,demographic.gender,demographic.race,demographic.ethnicity,case_id,summary.data_categories.file_count,summary.data_categories.data_category&filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22%3D%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%22TCGA-DLBC%22%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22genes.gene_id%22%2C%22value%22%3A%5B%22ENSG00000143951%22%5D%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22ssms.consequence.transcript.annotation.impact%22%2C%22value%22%3A%5B%22HIGH%22%5D%7D%7D%5D%7D&pretty=true&size=2"

curl "https://api.gdc.cancer.gov/analysis/top_mutated_cases_by_gene?gene_ids=ENSG00000092345&fields=
diagnoses.primary_diagnosis,
demographic.gender,
demographic.race,
demographic.ethnicity,
case_id,
summary.data_categories.file_count,
summary.data_categories.data_category&pretty=true"

'''

























#
