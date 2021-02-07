"""
Find the CAI(Codon Adaptive Index) for a given sequence.

Equation
------------
For each amino acid in a gene, the weight of each codon
is represented by a parameter termed relative adaptiveness
(wi) given a reference sequence set(codon_frequency.csv).
Ratio between observed frequency of codon fi and
Frequency of the most frequent synonymous codon fj for
That amino acid
fi = frequency of codon fi in a gene
fj = frequency of most frequent codon fj for that amino acid.
wi = fi/max(fj)
L = number of codons
CAIfi = geometric mean(wi)^(1/L)
CAImax = geometric mean(wmax)*1/L

Example: CCG, GTA, ATT, AAA, GTA
GTA: wi = 0.495, fmax = 1.111/0.495
CAIobs = (3.288 x 1.111 x 0.466 x 1.596 ....)^1/70
CAImax = (3.288 x 2.244 x 2.525 .....)^1/70
CAI = geometric mean(wk)^1/L
"""
import csv
from Bio import SeqUtils, SeqIO
from Bio import SeqIO
from Bio.SeqUtils import CodonUsage
from Bio.SeqUtils.CodonUsage import CodonAdaptationIndex

genePATH = "COVID_VACCINE/SARS-CoV.fasta" # Path to full genome of SARS-CoV
amino_acid = "COVID_VACCINE/ncov-s.fasta" # Path to Pfizer vaccine sequence
cd = SeqIO.read(genePATH, "fasta").seq
print(len(cd), len(cd) % 3)

# Because this is occurring in the human system, we will use a standard codon frequency table:
freq_table_path = "COVID_VACCINE/codon_frequency.csv"

# To turn string to float with catch, see: https://stackoverflow.com/questions/379906/how-do-i-parse-a-string-to-a-float-or-int
def conv_float(value):
  try:
    return float(value)
  except:
    return 0 # Default value

f = open(freq_table_path, "r").read().split("\n")
fz = {i[0]: [conv_float(ii) for ii in i[2:]] for i in map(lambda x: x.split(","), f[1:])}

# Calculate CAI
c = SeqUtils.CodonUsage.CodonAdaptationIndex()
# Open Pfizer vaccine sequence
c.generate_index(genePATH)
c.print_index()
read_seq = str(SeqIO.read(amino_acid, "fasta").seq)

print(c.cai_for_gene(read_seq))