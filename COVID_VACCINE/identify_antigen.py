"""
Given a .gb of a full genome sequence, do one of the following:
1) View features available and extract given structural protein
2) Identify structural protein to extract given lookup table()
"""
# Imports
from Bio import SeqIO

gbFile = "COVID_VACCINE/SARS-CoV.gb"  # Path to .gb file
featureI = "S"  # Feature to search for

class featureExtract:
    """
    Initialize feature extraction class.
    """

    def __init__(
        self,
        gbFile: "Path to .gb file",
        featureI: "Feature to search for"
    ):
        # Read GenBank of full genome sequence
        self.record = list(SeqIO.parse(gbFile, "genbank"))[0]
        # Feature to search for in self.search_through qualifiers in self.record
        self.feature = featureI
        # Where in qualifiers to search for features
        self.search_through = ["product", "gene", "note", "gene_synonym"]
        # Where the extracted features will get pushed to
        self.feature_extract = []
    """
    Search through genome sequence and extract features that match with the search query.
    """
    def search(self):
        # Looping through features
        for feat in self.record.features:
            # Loop through qualifiers
            for ii in self.search_through:
                # If the qualifier exists for this particular feature
                if ii in feat.qualifiers:
                    # If this qualifier contains search query
                    for iii in feat.qualifiers[ii]:
                        if self.feature in iii:
                            # Push to extracted features array
                            self.feature_extract.append([iii, ii, str(feat.extract(self.record).seq)])
        return self.feature_extract
    """
    Print out the qualifier name and the corresponding nucleotide sequence in a nice format.
    """

    def printI(
        self,
        len_to_print=50
        ):
        for i in self.feature_extract:
            print(F"{i[0]} - {i[1]}")
            print("".join(["-" for i in range(4 + len(F"{i[0]} - {i[1]}"))]))
            if len(i[2]) >= len_to_print:
                print(F"{i[2][0:int(len_to_print/2)]}...{i[2][-int(len_to_print/2):]}\n\n")
            else:
                print(F"{i[2]}\n\n")
            
# For debugging purposes
# l = featureExtract(gbFile, featureI)
# l.search()
# l.printI()