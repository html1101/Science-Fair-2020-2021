**Comparing virus to vaccine:**

Nucleotide differences:
        1061
        Nucleotide: 72% similarity
Protein differences:
        2
        Protein: 99.8% similarity
Codon differences:
        922
        Codon: 28% similarity
Overall: Not very similar.

**Comparing codon_mapping to vaccine:**
Nucleotide differences:
        330
        Nucleotide: 91% similarity
Protein differences:
        2
        Protein: 99.8% similarity
Codon differences:
        263
        Codon: 79% similarity

**Comparing discrete optimization to vaccine:**
Version 1:
Nucleotide differences:
        1288
        Nucleotide: 66% similarity
Protein differences:
        2
        Protein: 99.8% similarity
Codon differences:
        1068
        Codon: 16% similarity
GC Differences:
        4.4% difference

Version 2(window of size 10):
Nucleotide differences:
	554
	Nucleotide: 86% similarity
Protein differences:
	2
	Protein: 99.8% similarity
Codon differences:
	475
	Codon: 63% similarity
GC Differences
        4.2% difference

Window of size 12:
        4.9% difference
Window of size 8:
        3.7% difference but more codon diff
Window of size 9:
        2.2% difference



Discrete optimization - Version 2
Final Fitness: -0.005885
GC Content: 57.01%
Codon Freq: 14.95%
Nucleotide diff: 11.8% different
Codon diff: 28.728% different

Discrete optimization - Version 3(var of 0.2)
Change at pos 2922 from TCT to TCT
Final Fitness: 0.15171
GC Content: 57.67%
Codon Freq: 15.19%
Nucleotide diff: 12.4% different
Codon diff: 25.432% different

Final Fitness: 0.152201(var 0.4)
GC Content: 59.63%
Codon Freq: 15.29%
Nucleotides: 90.7% similar
Codons: 78.1% similar
Wrote to graphing.csv file
Wrote to /Users/sarah/Desktop/Science Fair 2020-2021/COVID_VACCINE/discrete_ver2.fasta
4037.616352081299

Discrete optimization ver 3(var 0.3 and no codon freq)
Solution appears not convex.
Final Fitness: 1.0
GC Content: 57.01%
Codon Freq: 13.37%
Nucleotides: 82.1% similar
Codons: 53.061% similar
Wrote to /Users/sarah/Desktop/Science Fair 2020-2021/COVID_VACCINE/discrete_ver3_var0.3_noFreq.csv file
Wrote to /Users/sarah/Desktop/Science Fair 2020-2021/COVID_VACCINE/discrete_ver3_var0.3_noFreq.fasta
4148.856741666794 seconds

Discrete optimization ver 3(var 0.3 * codon freq)
Solution appears not convex.
Final Fitness: 0.151915
GC Content: 58.48%
Codon Freq: 15.23%
Nucleotides: 89.0% similar
Codons: 76.06% similar
Wrote to /Users/sarah/Desktop/Science Fair 2020-2021/COVID_VACCINE/discrete_ver3_var0.3_FreqMult.csv file
Wrote to /Users/sarah/Desktop/Science Fair 2020-2021/COVID_VACCINE/discrete_ver3_var0.3_FreqMult.fasta
5865.575006723404 seconds

Discrete optimization ver 3(var 0.3 + codon freq)
Change at pos 2931 from AAC to AAC
Solution appears not convex.
Final Fitness: 1.151578
GC Content: 57.27%
Codon Freq: 15.17%
Nucleotides: 87.4% similar
Codons: 74.254% similar
Wrote to /Users/sarah/Desktop/Science Fair 2020-2021/COVID_VACCINE/discrete_ver3_var0.3_FreqAdd.csv file
Wrote to /Users/sarah/Desktop/Science Fair 2020-2021/COVID_VACCINE/discrete_ver3_var0.3_FreqAdd.fasta
5840.560879945755 seconds

Discrete optimization ver 3(var 0.3 + codon freq, alpha)
Solution appears not convex.
Final Fitness: 0.830284
GC Content: 57.06%
Codon Freq: 15.14%
Nucleotides: 88.4% similar
Codons: 74.019% similar
Wrote to /Users/sarah/Desktop/Science Fair 2020-2021/COVID_VACCINE/discrete_ver3_var0.3_FreqAddAlpha0.8.csv file
Wrote to /Users/sarah/Desktop/Science Fair 2020-2021/COVID_VACCINE/discrete_ver3_var0.3_FreqAddAlpha0.8.fasta
5208.715737104416 seconds


Vaccine
-------------------
Final Fitness: 0.147276
GC Content: 56.99%
Codon Freq: 14.73%
Nucleotides: 100.0% similar
Codons: 100.0% similar

