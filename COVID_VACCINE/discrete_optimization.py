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
import os, math

# plt.ion()
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

# For graphing later on
x = []
gcContMapY = []
fitnessMapY = []
nucleotideMapY = []
codonFreqMapY = []
codonMapY = []
"""
fig, axes = plt.subplots(2, 2)


axes[0, 0].set_ylim(0, 1)
axes[0, 0].set_xlim(0, 1000)
axes[0, 1].set_ylim(0, 1)
axes[0, 1].set_xlim(0, 1000)
axes[1, 0].set_ylim(0, 1)
axes[1, 0].set_xlim(0, 1000)
axes[1, 1].set_ylim(0, 1)
axes[1, 1].set_xlim(0, 1000)
"""
# fig.canvas.draw()
# plt.show(block=False)
"""
Class OptimizeSeq does the following:
__init__(seq) - Initializes and inputs a sequence(the section of the virus we are encoding)
change(val) - change the sequence to val
gc_content() - Calculates the GC content of the particular sequence(self.seq)
codon_freq() - Calculates the average frequency of that codon within the human body
fitness(alpha, expected_GC) - Calculates the fitness of the sequence through GC and Freq
stochastic_descent() - Use stochastic gradient descent to increase fitness
print_info(include header) - Print Fitness, GC content, amino acid frequency calcs from the current sequence.
"""
class OptimizeSeq:
    # Initializes and inputs a sequence(the section of the virus we are
    # encoding)
    def __init__(self, seq):
        self.seq = list(seq)
        self.var = 0.2
    
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
    def codon_freq(self):
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
    def fitness(self, expectedGC=0.57):
        # Find diff of expectedGC from gc content
        delta_gcFit = (expectedGC - self.gc_content())
        # Square and divide by variability**2
        prob_gcFit = math.exp(-delta_gcFit**2 / (self.var**2))
        prob_frequencyFit = self.codon_freq()
        return prob_gcFit * prob_frequencyFit

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
    def print_info(self, header=True, vacComp=True):
        if header:
            print("EVALUATE RESULTS")
            print("-------------------")
        fit = self.fitness()
        gc = self.gc_content()
        codonf = self.codon_freq()
        print(F"Final Fitness: {round(fit*1000000)/1000000}")
        print(F"GC Content: {round(gc*10000)/100}%")
        print(F"Codon Freq: {round(codonf*10000)/100}%")
        if vacComp:
            comp_nucleo, comp_codon = self.compare() # Compare to vaccine
            print(F"Nucleotide diff: {round(comp_nucleo*1000)/10}% different")
            print(F"Codon diff: {round(comp_codon*100000)/1000}% different")

        return fit, gc, codonf, comp_nucleo, comp_codon

    def graphInfo(self, path="graphing.csv"):
        # Calc printInfo, push into the graphs
        x.append(len(x)+1) # Represents # iterations made
        fitnessY, gcContY, codonFreqY, nucleotideY, codonY = self.print_info(header=False, vacComp=True)
        fitnessMapY.append(str(fitnessY))
        gcContMapY.append(str(gcContY))
        codonFreqMapY.append(str(codonFreqY))

        # Comparing with vaccine
        nucleotideMapY.append(str(nucleotideY))
        codonMapY.append(str(codonY))
        
        # Write to graphing file
        f = open(path, "w+")
        f.write(",".join(fitnessMapY) + "\n")
        f.write(",".join(gcContMapY) + "\n")
        f.write(",".join(codonFreqMapY) + "\n")
        f.write(",".join(nucleotideMapY) + "\n")
        f.write(",".join(codonMapY) + "\n")
        f.close()
        print(F"Wrote to {path} file")


    """
    Use stochastic gradient descent. Does the following:
    - Looks at codon at pos x, finds the amino acid it encodes for, and finds all possible codons
    that could encode for that same amino acid.
    - Go through all codon possibilities and calculate the fitness on the entire sequence.
    - Go through the whole process, marking the change that makes the lowest fitness.
    - Make the change with the lowest fitness and repeat.
    - Stores values in file path
    """
    def discrete_descent(self, print_output = False, filePath = dir + "COVID_VACCINE/stochas.fasta"):
        best_solution = [0, 0, 0] # [fitness, pos, change to]
        past_fit = float("inf") # To find when the fitness reaches a local minima
        current_iters = 0
        while not best_solution[0] == past_fit:
            past_fit = best_solution[0]
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
                    if this_fitness > best_solution[0]:
                        best_solution = [this_fitness, int(i), possibleCodon]
                # Change back to original codon
                self.change(i, originalCodon)
            # Print best solution, make corresponding changes, and run again.
            if print_output:
                print(F"\nIter #{current_iters} Optimized: {abs(best_solution[0] - past_fit)}")
                print("----------------------------")
                print(F"Change at pos {best_solution[1]} from {''.join(self.seq[best_solution[1]:best_solution[1]+3])} to {best_solution[2]}")
                self.graphInfo()
                # Write to file
                w = open(filePath, "w+")
                w.write(F">discrete gradient descent vaccine\n")
                w.write("\n".join(["".join(self.seq[i:i+75]) for i in range(0, len(self.seq), 75)]))
                w.close()
                print(F"Wrote to {filePath}")
            self.change(*best_solution[1:])
            current_iters += 1

        return self.seq

# **EVALUATING**
# (Because Python isn't async we need this after the object)
# Evaluate on a random string of len Spike
import random
choi = ['A']
randomStr = [random.choice(choi) for i in range(len(Spike[:111]))]
optim = OptimizeSeq(randomStr)

x, y = [], []
for i in range(len(randomStr)):
    optim.seq[i] = "C"
    # Calculate new fitness
    x.append(i)
    y.append(optim.fitness())

plt.plot(x, y)
plt.show()

# Run OptimizeSeq on Spike
optimize = OptimizeSeq(Spike)
print(len(Spike))
print(optimize.print_info())
# Run optimization
optimize.discrete_descent(True, dir + 'COVID_VACCINE/discrete_ver2.fasta')

"""

# Run OptimizeSeq on Spike
optimize = OptimizeSeq(Spike[:111])
print(len(Spike))
print(optimize.print_info())
# Run optimization
optimize.discrete_descent(True, dir + 'COVID_VACCINE/discrete_ver1.fasta')

Calculate the number of iterations:
We're modifying codon-by-codon from the spike.
This means that we can start by calulating the # differences

results = optimize.discrete_descent(print_output=True)
print("".join(results))
optimize.print_info()
"""

# Optimize the fitness function by modifying alpha values
"""
- Run vac through fitness with alpha value n.
- Goal: Minimize fitness through stochastic gradient descent.
"""
import numpy as np

actual_vac = OptimizeSeq(Vaccine)
actual_vac.print_info()

# Start from this point, then step forwards by step_size.

"""
derivative = (d(x+h)+d(x))/h
h = step size
"""
# Find fitness

# Create graph comparing alpha values and their fitness
"""
alphaX = np.arange(-0, 1, 0.1)
fitnessY = []
for i in alphaX:
    fitnessY.append(actual_vac.fitness(alpha=i))

plt.plot(alphaX, fitnessY)
plt.show()
"""