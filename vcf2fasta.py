#!/usr/bin/env python3
import gzip
import argparse
import pandas as pd
from Bio import SeqIO
from Bio import pairwise2
from Bio.pairwise2 import format_alignment


parser = argparse.ArgumentParser()
parser.add_argument('-g','-G','--genome')
parser.add_argument('-v','-V','--vcf')
parser.add_argument('-t','-T','--table')

##获取参数
args = parser.parse_args()
Genome = args.genome
VCF_file = args.vcf
Target = args.table

def get_vcf_names(vcf_path):
    with gzip.open(vcf_path, "rt") as ifile:
          for line in ifile:
            if line.startswith("#CHROM"):
                  vcf_names = [x for x in line.split('\t')]
                  break
    ifile.close()
    return vcf_names

SAMPLE = VCF_file.replace(".vcf.gz", "")
names = get_vcf_names(VCF_file)
vcf = pd.read_csv('G1FFH.vcf.gz', compression='gzip', comment='#',  header=None, names=names, sep='\t')

TARGET = pd.read_csv(Target, sep='\t')

for seq_record in SeqIO.parse(Genome, "fasta"):
    if seq_record.id in TARGET.CHROM.unique():
        print("Chrom:", seq_record.id)
        TB = pd.DataFrame([*seq_record.seq])
        TB['REF'] = ""
        TB['ALT'] = ""
        TB.iloc[vcf.POS-1,1] = vcf.REF.to_list()
        TB.iloc[vcf.POS-1,2] = [i.split(",")[0] for i in vcf.ALT.to_list()]
        TB.ALT[TB.ALT==""] =  TB[0][TB.ALT==""].to_list()
        TB.head()
        TB["Len"] = [len(i)-1 for i in TB.REF]
        TB.Len[TB.Len<0]=0

        TB["DEL"] = 0
        TB["DEL_mark"] = 0

        TB.DEL =TB.Len.to_list()[:1] +TB.Len.to_list()[:-1]
        TB.DEL_mark += TB.DEL
        TB.DEL[TB.DEL>1] = TB.DEL_mark[TB.DEL>1]-1
        while TB.DEL.max()!=0:
            TB.DEL =TB.DEL.to_list()[:1] +TB.DEL.to_list()[:-1]
            TB.DEL_mark += TB.DEL
            TB.DEL[TB.DEL>0] = TB.DEL[TB.DEL>0]-1

        TMP = TB.ALT[TB.DEL_mark==0]
        F = open(SAMPLE + "_" + seq_record.id +".fa", "w")
        F.close()

        F = open(SAMPLE + "_" + seq_record.id +".fa", "a")
        LIST = []
        for i in range(len(TARGET[TARGET.CHROM==seq_record.id])):
            FROM =TARGET.START[TARGET.CHROM==seq_record.id][i]
            END = TARGET.END[TARGET.CHROM==seq_record.id][i]
            print(FROM,END)
            STR1 = "".join(TB[0][TB.index.isin(range(FROM-1,END))].to_list())
            STR2 = "".join(TMP[TMP.index.isin(range(FROM-1,END))].to_list())
            F.write(">"+TARGET.NAME[TARGET.CHROM==seq_record.id][i] + "_" + SAMPLE + "\n" + STR2 + "\n" )
            LIST += range(FROM-1,END)

        F.write(">NonHit_" + SAMPLE + "\n" + "".join(TMP[~TMP.index.isin(LIST)]) + "\n" )

        F.close()

        # Print Alignment results
        #alignments = pairwise2.align.globalxx(STR1, STR2)
        #print(format_alignment(*alignments[0]))
