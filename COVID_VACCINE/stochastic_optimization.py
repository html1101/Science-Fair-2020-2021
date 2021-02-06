"""
This uses a GA to do the following:
1) Manage GC ratio(between 50% and 65% as done in BNT)
2) Codon optimization

"""
from Bio import SeqIO
from Bio.SeqUtils import MeltingTemp as mt
import json
import matplotlib
import matplotlib.pyplot as plt
import os

# Directory for debugging
dir = "/Users/sarah/Desktop/Science Fair 2020-2021/"

# Path to codon => amino acid lookup table
PATH_codon_to_protein = dir + "COVID_VACCINE/codon_to_protein.json"
# Path to genomic sequence of SARS-CoV virus
Spike_PATH = dir + "COVID_VACCINE/ncov-s.fasta"
# Path to Pfizer vaccine genomic sequence
Vac_PATH = dir + "COVID_VACCINE/vaccine-s.fasta"
# Path to codon mapping solution lookup table
PATH_codon_map = dir + "COVID_VACCINE/vaccine_dict.json"
# Path to codon frequency lookup table
PATH_codon_freq = dir + "COVID_VACCINE/codon_frequency.csv"

# Read and convert spike path to sequence
Spike = str(SeqIO.read(open(Spike_PATH, "r"), "fasta").seq)
# Read and convert vaccine path into sequence
Vaccine = str(SeqIO.read(open(Vac_PATH, "r"), "fasta").seq)

# Opening the codon => amino acid lookup table and converting it to JSON format
"""
JSON format:
{
"amino acid": [arr of all possible codons]
}
"""
codonAmino = json.loads(open(PATH_codon_to_protein, "r").read())
revCodonAmino = {}
for i, j in codonAmino.items():
    if j in revCodonAmino:
        revCodonAmino[j].append(i)
    else:
        revCodonAmino[j] = [i]
print(codonAmino)

# Opening the codon => frequency in human body lookup table and converting to
"""
JSON format:
{
"codon": 0.45
}
"""
codonFreqArr = open(PATH_codon_freq, "r").read().split("\n")[1:] # Take out header
codonFreq = {}
for i in codonFreqArr:
    line = i.split(",")
    # line[0] uses Us instead of Ts; because we're using RNA, we need to replace them.
    line[0] = line[0].replace("U", "T")
    codonFreq[line[0]] = float(line[2])

print(codonFreq)

"""
Class OptimizeSeq does the following:
__init__(seq) - Initializes and inputs a sequence(the section of the virus we are encoding)
change(val) - change the sequence to val
gc_content() - Calculates the GC content of the particular sequence(self.seq)
amino_acid_freq() - Calculates the average frequency of that codon within the human body
fitness(alpha, expected_GC) - Calculates the fitness of the sequence through GC and Freq
stochastic_descent() - Use stochastic gradient descent to increase fitness
print_info(include header) - Print Fitness, GC content, amino acid frequency calcs from the current sequence.
"""
class OptimizeSeq:
    # Initializes and inputs a sequence(the section of the virus we are
    # encoding)
    def __init__(self, seq):
        self.seq = list(seq)
    
    # Change self.seq at pos x to val
    def change(self, x, val):
        self.seq[x:x+len(val)] = list(val)
        return self.seq
    
    # Calculates the GC content of the particular sequence(self.seq)
    def gc_content(self):
        gc_count = 0
        # Add all the Gs and Cs within the sequence, then divide by len(seq)
        # One liner: len(list(filter(lambda x: x == "G" or x == "C",
        # self.seq)))
        for i in self.seq:
            if i == "G" or i == "C":
                gc_count += 1
        return gc_count / len(self.seq)
    
    # Calculates the average frequency of the codons in the optimized vaccine
    # in the human body
    def amino_acid_freq(self):
        # Add all the frequencies within the sequence and div by len(seq)
        added_frequencies = 0
        
        # Iterate through codons
        for codonS in range(0, len(self.seq), 3):
            added_frequencies += codonFreq["".join(self.seq[codonS:codonS+3])]
        
        return added_frequencies / len(self.seq)

    """
    Calculates the fitness of the sequence by the following:
    - GC content - Inputting the actual GC content, finds the GC by MSE
    - Frequency - How frequent the particular codon is in the homan body.
    - Do weighted addition with alpha.
    """
    def fitness(self, alpha=0.8, expectedGC=0.57):
        # Squaring makes values get too large too fast
        gcFit = abs(expectedGC - self.gc_content())
        frequencyFit = (1 - alpha)*self.amino_acid_freq()
        return alpha*gcFit + (1-alpha)*frequencyFit

    # Compare nucleotide and codon % differences to the actual vaccine
    def compare(self, vaccine=Vaccine):
        nucleotide_count = 0
        codon_count = 0
        for i in range(0, len(self.seq), 3):
            # Iterate through codons and compare codons
            if not "".join(self.seq[i:i+3]) == vaccine[i:i+3]:
                codon_count += 1
            # Iterate through nucleotides within the codon(because we're
            # doing this in o(n) time).
            for ii in range(i, i+3):
                if not self.seq[ii] == vaccine[ii]:
                    # Different nucleotides
                    nucleotide_count += 1
        return nucleotide_count / len(vaccine), codon_count / (len(vaccine)/3)

    # Print Fitness, GC content, amino acid frequency, nucleotide, and codon calcs from the current sequence.
    def print_info(self, header=True):
        if header:
            print("EVALUATE RESULTS")
            print("-------------------")
        print(F"Final Fitness: {round(self.fitness()*1000000)/1000000}")
        print(F"GC Content: {round(self.gc_content()*10000)/100}%")
        print(F"Amino Acid Freq: {round(self.amino_acid_freq()*10000)/100}%")
        comp_nucleo, comp_codon = self.compare() # Compare to vaccine
        print(F"Nucleotide diff: {round(comp_nucleo*1000)/10}% different")
        print(F"Codon diff: {round(comp_codon*100000)/1000}% different")

        return self.fitness(), self.gc_content(), self.amino_acid_freq()

    """
    Use stochastic gradient descent. Does the following:
    - Looks at codon at pos x, finds the amino acid it encodes for, and finds all possible codons
    that could encode for that same amino acid.
    - Go through all codon possibilities and calculate the fitness on the entire sequence.
    - Go through the whole process, marking the change that makes the lowest fitness.
    - Make the change with the lowest fitness and repeat.
    """
    def stochastic_descent(self, max_iters = 100, print_output = False):
        best_solution = [float("inf"), 0, 0] # [fitness, pos, change to]
        current_iters = 0 # To print out total iters
        while not current_iters > max_iters:
            for i in range(0, len(self.seq), 3):
                originalCodon = list(self.seq[i:i+3]) # Original codon to revert back to
                # Iterate through all virus codons and codons that produce the same amino acid.
                # Converting codon => amino => all codons that encode for that amino
                amino_acid = codonAmino["".join(self.seq[i:i+3])]
                for possibleCodon in revCodonAmino[amino_acid]:
                    # Change seq to this particular codon
                    self.change(i, possibleCodon)
                    # Check its fitness
                    this_fitness = self.fitness()
                    # If it does well, store it.
                    if this_fitness < best_solution[0]:
                        best_solution = [this_fitness, int(i), possibleCodon]
                # Change back to original codon
                self.change(i, originalCodon)
            # Print best solution, make corresponding changes, and run again.
            if print_output:
                print(F"\n\nIteration {current_iters} of {max_iters}")
                print("----------------------------")
                print(F"Change at pos {best_solution[1]} from {''.join(self.seq[best_solution[1]:best_solution[1]+3])} to {best_solution[2]}")
                self.print_info(header=False)
            self.change(*best_solution[1:])
            current_iters += 1

        return self.seq

"""
**EVALUATING**
(Because Python isn't async we need this after the object)
"""
# Run OptimizeSeq on Spike
optimize = OptimizeSeq(Spike)

"""
ATTGCC
GC cont: 50%
Ideal: 57%
ATT
"""
results = optimize.stochastic_descent(max_iters=100, print_output=True)
print("".join(results))
optimize.print_info()

# Compare to actual vaccine; we won't run optimization, but we will use the same GC and freq functions.
# actual_vac = OptimizeSeq(Vaccine)
# actual_vac.print_info()