#!/usr/bin/env python3

import argparse, os
from Bio.Align.Applications import ClustalwCommandline
from Bio import AlignIO
from Bio import Phylo


parser = argparse.ArgumentParser()
parser.add_argument('-i','-I','--input',
    help = "Input fasta file please| 输入文件")    #输入文件
parser.add_argument('-o','-O','--output',
    help = "输出文件前缀",
    default = "Karobben")     #输入文件
parser.add_argument('-t','-T','--tree',
    help = "NJ | UPGMA; default = NJ",
    default = "NJ")     #输入文件
parser.add_argument('-s','-S','--tree_size',
    help = "w,h size of the tree png; default = 7,7",
    default = "7,7")     #输入文件

##获取参数
args = parser.parse_args()
INPUT  = args.input
OUTPUT = args.output
ARG_TREE = args.tree
ARG_TREE_SIZE = args.tree_size


## Pre-align

cwline = ClustalwCommandline("clustalw", infile= INPUT, outfile = OUTPUT + ".fasta",  output= "fasta" )
print(cwline)
stdout, stderr = cwline()

## reading the alignments
align = AlignIO.read(OUTPUT + ".fasta", "fasta")

## Count the longest space on the head

Gap_head = 0
Gap_tail = 0
Gap_list_head = []
Gap_list_tail = []
for seq_tmp in align:
    Num = 0
    while seq_tmp[Num] == "-":
        Num +=1
    Gap_list_head += [Num]
    if Num > Gap_head:
        Gap_head = Num
## Count the longest space on the tail
for seq_tmp in align:
    Num = 0
    while seq_tmp[::-1][Num] == "-":
        Num +=1
    Gap_list_tail += [Num]
    if Num > Gap_tail:
        Gap_tail = Num

print("\nGap head list: ", Gap_list_head,
      "\nGap head tail: ", Gap_list_tail)
print("\nGap head: ", Gap_head,
      "\nGap head: ", Gap_tail)

## Count the longest space on the head


# Alignment objects can be manipulated

# slice alignment
align_slice = align[:, Gap_head : len(seq_tmp)-Gap_tail]
print ("Slice of alignment from position " + str(Gap_head) + " to " + str(Gap_tail) +"\n")
print(align_slice)

## wirte it out
F = open(OUTPUT + "_scliced.fa", 'w')
F2 = open(OUTPUT + "_gap.fa", 'w')
for Seq_tmp in align_slice:
    F.write(">" + Seq_tmp.id+"\n")
    F2.write(">" + Seq_tmp.id+"\n")
    Seq_seq = str(Seq_tmp.seq)
    F2.write(Seq_seq+"\n")
    Seq_seq = Seq_seq.replace("-","")
    F.write(Seq_seq+"\n")
F.close()
F2.close()


##
# Make Phylogenetic Tree

cwline = ClustalwCommandline("clustalw", infile= OUTPUT + "_gap.fa",  clustering = ARG_TREE, bootstrap = 1000)
print(cwline)
stdout, stderr = cwline()


tree = Phylo.read(OUTPUT.split(".")[0]+"_gap.phb", "newick")
Phylo.draw_ascii(tree)

# select the 3 sequences in the top branch of phylo tree

align_branch = align_slice[0:3]
print(align_branch)

### save the tree as png
PATH_lib = os.path.dirname(__file__)

R_w = ARG_TREE_SIZE.split(",")[0]
R_h = ARG_TREE_SIZE.split(',')[1]

R_ARG = "##".join([OUTPUT+"_gap.phb",
        R_w , R_h])


CMD = "Rscript " + PATH_lib + "/lib/R/ggtree.R " + R_ARG
print(CMD)
os.system(CMD)
