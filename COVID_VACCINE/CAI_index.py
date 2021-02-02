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

genePATH = "COVID_VACCINE/ncov-s.fasta.txt" # Path to full genome of SARS-CoV
amino_acid = "COVID_VACCINE/vaccine-s.fasta.txt" # Path to Pfizer vaccine sequence

# Because this is occurring in the human system:
freq_table = "COVID_VACCINE/"