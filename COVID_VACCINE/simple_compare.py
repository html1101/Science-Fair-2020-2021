"""
Given two sequences, compare the two by the following:
- Protein comparison - How similar the corresponding protein sequence is.
- RNA comparison - How similar the RNA sequences are, nucleotide by nucleotide.
- Codon differences - How similar the codon sequences are.
"""

from scipy.stats import norm

class SequenceComp:
    def __init__(
            self,
            seq_1, # The first sequence to compare; this is the predicted sequence.
            seq_2): # The second sequence to compare.
        self.seq_1 = seq_1
        self.seq_2 = seq_2
        # assert len(self.seq_1) == len(self.seq_2)

    # Compare the two RNA sequences are, nucleotide by nucleotide.
    def rna_compare(self):
        loc_differ = ""
        num_differences = 0
        for i in range(min(len(self.seq_1), len(self.seq_2))):
            if i < len(self.seq_1):
                if i < len(self.seq_2):
                    if self.seq_1[i] == self.seq_2[i]:
                        loc_differ += " "
                    else:
                        loc_differ += "!"
                        num_differences += 1
                else:
                    loc_differ += "!"
                    num_differences += 1
            else:
                loc_differ += "!"
                num_differences += 1
        return loc_differ, num_differences
    # def conv_to_protein(self):
    #     s = ""
    #     for i in range(0, len(self.seq), 3):
    #         s += codonProtein[self.seq[i:i+3]]
        # return s
    def protein_compare(
            self,
            codon_to_protein): # Dictionary with codon => protein
        loc_differ = ""
        translated_codons_pred = ""
        translated_codons_act = ""
        num_differences = 0
        for i in range(0, min(len(self.seq_1), len(self.seq_2)), 3):
            predicted_prot = codon_to_protein[self.seq_1[i:i+3]]
            actual_prot = codon_to_protein[self.seq_2[i:i+3]]
            translated_codons_pred += " " + predicted_prot + " "
            translated_codons_act += " " + actual_prot + " "
            if predicted_prot == actual_prot:
                loc_differ += "   "
            else:
                loc_differ += " ! "
                num_differences += 1
        return translated_codons_pred, translated_codons_act, loc_differ, num_differences

    def codon_compare(
            self):
        loc_differ = ""
        num_differences = 0
        for i in range(0, min(len(self.seq_1), len(self.seq_2)), 3):
            predicted_prot = self.seq_1[i:i+3]
            actual_prot = self.seq_2[i:i+3]
            if predicted_prot == actual_prot:
                loc_differ += "   "
            else:
                loc_differ += " ! "
                num_differences += 1
        return loc_differ, num_differences

    def print_compare(
            self,
            cod_to_prot,
            printFull=True): # Codon to protein dictionary and whether to include full output
        resultsN, diffN = self.rna_compare()
        codP, codA, resultsP, diffP = self.protein_compare(cod_to_prot)
        codonC, codonD = self.codon_compare()
        if printFull:
            for i in range(0, len(self.seq_1), 50):
                # Print out proteins for seq 1
                print(codP[i:i+50])
                # Print out sequence 1
                print(self.seq_1[i:i+50])
                # Print out nucleotide differences
                print(resultsN[i:i+50])
                # Print out sequence 2
                print(self.seq_2[i:i+50])

                # Print out proteins for seq 2
                print(codA[i:i+50])
                # Print out differences in proteins
                print(resultsP[i:i+50], end="\n\n\n")
        print(F"Nucleotide differences:\n\t{diffN}")
        print(
            F"\tNucleotide: {round((1-diffN/len(self.seq_1))*100)}% similarity")
        print(F"Protein differences:\n\t{diffP}")
        print(
            F"\tProtein: {round((1-(diffP/(len(self.seq_1)/3)))*1000)/10}% similarity")
        print(F"Codon differences:\n\t{codonD}")
        print(
            F"\tCodon: {round((1-(codonD/(len(self.seq_1)/3)))*100)}% similarity")
    def graph_nucleotides(
        self,
        frame=10, # Frame to measure nucleotides
    ):
        x, y = [], []
        for i in range(0, len(self.seq_1), frame):
            # Iterate through and measure nucleotide differences
            x.append(i)
            arr = [self.seq_1[ii] for ii in range(i, i+frame)]
            y.append(len(list(filter(lambda x: x == 1, arr))))
        return [x, y]
    def change_seq(
            self,
            name, # Name: either seq_1 or seq_2
            change_to): # New sequence to change to
        # self[name] = change_to
        setattr(self, name, change_to)