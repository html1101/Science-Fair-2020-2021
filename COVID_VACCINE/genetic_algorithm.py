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
from scipy.stats import norm
from simple_compare import SequenceComp
from codon_mapping import codon_optimize
import os

PATH_codon_to_protein = "COVID_VACCINE/codon_to_protein.json"
Spike_PATH = "COVID_VACCINE/ncov-s.fasta"
Vac_PATH = "COVID_VACCINE/vaccine-s.fasta"
PATH_codon_map = "COVID_VACCINE/vaccine_dict.json"


codonProtein = json.loads(open(PATH_codon_to_protein, "r").read())


class OptimizeSeq:
    def __init__(self, seq):
        self.seq = seq
    def graph_gc(self, frame=10):
        x, y = [], []
        for i in range(0, len(self.seq), frame):
            x.append(i)
            y.append(self.gc_content(self.seq, window=[i, i+frame]))
        plt.plot(x, y)
        # plt.show()
    def gc_content(self, seq=None, window=None):
        if not seq:
            seq = self.seq
        if not window:
            window = [0, len(seq)]
        # Evaluate the level of GC content within the S spike
        num_GC = len(list(filter(lambda x: x == "G" or x == "C", seq[window[0]:window[1]])))
        return num_GC / (window[1] - window[0])
    def norm_gc_cont(self, seq=None, window=None):
        if not seq:
            seq = self.seq
        if not window:
            window = [0, len(seq)]
        # Perform inverse normal to set -3-3 SD of GC content within window
        # scipy.stats.norm.cdf(x, mean, sd)
        # norm.ppf(area, mean, sd)
        # mean = mean(window), sd = (window[0]-mean)/+-3
        mean = (window[0] + window[1])/2
        sd = (window[1] - mean)/3
        # Find pdf of the particular GC content
        return norm.pdf(self.gc_content(), loc=mean, scale=sd)
    def calc_temp(self):
        # Calculate melting temperature for sequence
        return mt.Tm_NN(self.seq)
    def evaluate(self):
        # Given the type of loss(codon differences, protein diff, or nucleotide diff, find the loss)
        loss = 0
        best_found = list("ATCGGGTTAA")
        self.seq = best_found
        this_count = best_found
        best_loss = self.gc_content(best_found)
        changed = True
        while changed:
            changed = False
            for i in range(len(best_found)):
                for ii in ["A", "C", "G", "T"]:
                    this_count[i] = ii
                    this_loss = self.gc_content(this_count)
                    if this_loss > best_loss:
                        best_loss = this_loss
                        best_found = this_count
                        changed = True
                this_count = best_found
        return best_found

# Input: Genetic sequence to the spike
init_spike = str(SeqIO.read(Spike_PATH, "fasta").seq)
# For evaluation: Genetic sequence to the vaccine path
vac_encode = str(SeqIO.read(Vac_PATH, "fasta").seq)
k = OptimizeSeq(str(SeqIO.read(Spike_PATH, "fasta").seq))

# Version 0: Comparing the vaccine to the virus
l = SequenceComp(init_spike, vac_encode)
l.print_compare(codonProtein)

# Version 1: Comparing the vaccine to the codon map
optimized_spike = codon_optimize(init_spike, PATH_codon_map)
l.change_seq("seq_1", optimized_spike)
l.print_compare(codonProtein)

print(k.evaluate())