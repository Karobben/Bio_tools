#!/usr/bin/env python3
import gzip
import warnings
import argparse
import pandas as pd
from Bio import SeqIO
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('-g','-G','--genome')
parser.add_argument('-v','-V','--vcf')
parser.add_argument('-t','-T','--table')
parser.add_argument('-d','-D','--redirect', default='No',  nargs='?', help="Redorect sequence according to the table(+/-). default=Yes")
parser.add_argument('-s','-S','--verbos', default='Yes',  nargs='?', help="Pring logs. default=Yes")
parser.add_argument('-c','-C','--connect', default='No',  nargs='?', help="connect rest of gaps. default=No")

##获取参数
args = parser.parse_args()
Genome = args.genome
VCF_file = args.vcf
Target = args.table
Redirect = args.redirect
Verbos = args.verbos
Connect = args.connect

def Vprint(Str):
    if Verbos != "No":
        print(Str)

def get_vcf_names(vcf_path):
    with gzip.open(vcf_path, "rt") as ifile:
          for line in ifile:
            if line.startswith("#CHROM"):
                  vcf_names = [x for x in line.split('\t')]
                  break
    ifile.close()
    return vcf_names


if Verbos == None:
    Verbos = "No"
else:
    Verbos = "Yes"

if Redirect == None:
    Redirect = "Yes"
else:
    Redirect = "No"

if Connect == None:
    Connect = "Yes"
else:
    Connect = "No"


print("vcf2fasta.py -g", Genome, "-v", VCF_file, "-t", Target, "-d", Redirect, "-s", Verbos, "-c", Connect)

Vprint("Reading VCF file: " + VCF_file)
SAMPLE = VCF_file.replace(".vcf.gz", "")
names = get_vcf_names(VCF_file)
vcf = pd.read_csv('G1FFH.vcf.gz', compression='gzip', comment='#',  header=None, names=names, sep='\t')

Vprint("Reading Gene table: " + Target)
TARGET = pd.read_csv(Target, sep='\t')

Vprint("Start to replacing...")
for seq_record in SeqIO.parse(Genome, "fasta"):
    if seq_record.id in TARGET.CHROM.unique():
        Vprint(" ".join(["Chrom:", seq_record.id]))
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
            NAME = TARGET.NAME[TARGET.CHROM==seq_record.id][i]

            Vprint(" ".join([seq_record.id, str(i+1), NAME, str(FROM), str(END)]))

            STR1 = "".join(TB[0][TB.index.isin(range(FROM-1,END))].to_list())
            STR2 = "".join(TMP[TMP.index.isin(range(FROM-1,END))].to_list())
            if Redirect == "Yes" and TARGET.Dirc[TARGET.CHROM==seq_record.id][i] =="-":
                STR2 = STR2[::-1]
            F.write(">"+ NAME + "_" + SAMPLE + "\n" + STR2 + "\n" )
            LIST += range(FROM-1,END)

        if Connect == "Yes":
            F.write(">NonHit_" + SAMPLE + "\n" + "".join(TMP[~TMP.index.isin(LIST)]) + "\n" )

        F.close()

        # Print Alignment results
        #alignments = pairwise2.align.globalxx(STR1, STR2)
        #print(format_alignment(*alignments[0]))
