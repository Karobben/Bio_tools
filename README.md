# Karobben-Work-Station


| Scrips | Functions  | 中文|
| :------------- | :------------ | :- |
| Item One       | Item Two       | |
|[NCBI_GSM.PY](#NCBI_GSM)| I forget what's the function of this one = =|
|<a href="#Uniprot">Uniport.py</a> |Annotate your Uniprot ID|Uniport ID 的注释说明|
|<a href="#k2u">Kegg2Uniport.py</a> |From  *koID* to a *UniportID* list|把 KO 的 ID 转化成 Uniport ID|
|[Seq2tree.py](#seq2tree)| Quickest Pipeline to plot a tree from a fasta file with python and R script| 超快的fasta文件一键建树画图脚本|

## <a id="NCBI_GSM">NCBI_GSM.py</a>

This Script is designed for crawling GSM ID, GSM2268339 for instants, information form NCBI database.<br>
An example target website: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM2268339<br>
You can get the GSM ID, Title, Characteristics, et al, with a GSM list.<br>
But due to the unique information pattern of each GSM-group, try to fit the script by your
targets and test it before running it.

```
NCBI_GSM.py -i list -o result.csv
```
feel free


## <a id="Uniprot">Uniprot.py</a>

This script is for annotating the UNPROT ID by usring Python Crawler

Quick Start:
```
Uniprot.py -i list -o out.table(default)
```
Example
```
# Creat a Unprot_ID list
echo -e "Q9VVT4\nQ8T4H6\nQ9VN56\nQ9VLB2\nQ9VFE6\nQ6IG51\nQ9VQS1\nR9PY49\nQ8T4D4\nA0A0B4LGT9\nQ9VHV6\nB7Z003\nA0A0S0WGV8\nP54366\nA0A0B4K6X9\nQ7K0E3\nQ9VAU9\nN0D8I3\nQ9W420\nP52654\nF0JAF9\nQ7KNM2" \
> list
# Run Script
Uniprot.py -i list
# Viewresult
cat out.table
```
list:

||
|:---|
|Q8T4D4|
|Q8T4H6|
|P54366|
|Q9VFE6|
|...|

Result:

|Uniprot ID|Symbol|Protein|Species|Details|
|:---|:---|:---|:---|:---|
|Q9VFE6|CG3817|RRP15-like protein|Drosophila melanogaster (Fruit fly)|Belongs to the RRP15 family.Curated|
|Q9VAU9|Noa36|Zinc finger protein 330 homolog|Drosophila melanogaster (Fruit fly)|NucleusNucleus  By similaritynucleolus  By similarityNote: Predominantly expressed in the nucleolus.By similarity|
|Q8T4D4|Dmel\CG9222|AT03158p|Drosophila melanogaster (Fruit fly)|Belongs to the protein kinase superfamily.UniRule annotationAutomatic assertion according to rulesiRuleBase:RU000304|
|P54366|Gsc|Homeobox protein goosecoid|Drosophila melanogaster (Fruit fly)|Appears to regulate regional development of specific tissues. Can rescue axis polarity in UV-radiated Xenopus embryos.|
|...|...|...|...|...|

***PS: You might lost some entries duto the internet problem. My suggestion is Collecting the entries and run it again.***

## <a id="k2u">Kegg2Uniport.py</a>

This script can help you to turn KoID to UniportID
example:
```bash
/media/ken/Data/Github/Bio_tools/Kegg2Uniprot.py -i 10305
```
<span style="Background:salmon">backs to:</span>
```bash
K10305	FBXO25_32; F-box protein 25/32	Name
A0A024R9F3	A0A024R9F3_HUMAN	F-box protein 32, isoform CRA_c
A0A074ZPR8	A0A074ZPR8_9TREM	F-box domain protein
A0A088AP91	A0A088AP91_APIME	Uncharacterized protein
A0A094ZG88	A0A094ZG88_SCHHA	F-box domain-containing protein
...
```

## <a id="seq2tree">Seq2tree.py</a>

More details: [More details: Blog](https://karobben.github.io/2021/10/22/Bioinfor/biopython-seq2tree/)

Rely:
- python: Biopython;
- R: ggtree

Pipeline:
1. Biopython use clustalw2 to align fasta file
2. Trimming the gap from head and tail
3. Build tree file with trimmed sequences
4. Visualizing tree through ggtree with R

![Quick Tree](https://z3.ax1x.com/2021/10/23/5g649f.png)
