# Karobben-Work-Station

<a href="#NCBI_GSM">NCBI_GSM.PY</a> (I forget what's the function of this one = =)

<a href="#Uniprot">Uniport.py</a>  (Annotate your Uniprot ID)

## <a id=NCBI_GSM>NCBI_GSM.py</a>

NCBI_GSM.py is a scrip for grepping the information from the NCBI database. Since the format per GSE is so different. So you need to change the code to fit your purpose. Since the IP will probably be locked or limited by the NCBI because of frequency requests, I didn't apply the multiprocessing on here. 

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

***PS: You might lost some entries duto the internet problem. My suggestion is Collecting the entries and run it again. ***
