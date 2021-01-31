# Inspired by Harry Harpel's codon map.
# Concept: A codon mapping dictionary to optimize GC content within the vaccine.
import json
from absl import app
from absl import flags # To pass arguments
import time
from simple_compare import SequenceComp 

FLAGS = flags.FLAGS

# flags.DEFINE_string('output', "COVID_VACCINE/Seq", 'Name of file to push to + .fasta. Default file.fasta.')
flags.DEFINE_boolean('compare', False, "Whether or not to compare to real vaccine.")
flags.DEFINE_string('file', 'COVID_VACCINE/ncov-s.fasta.txt', "Name of file to read from. Default Sars-CoV virus.")
flags.DEFINE_string('debug', 'COVID_VACCINE/vaccine-s.fasta.txt', "Name of file to use for comparison. Default Sars-CoV vaccine.")

PATH_codon_map = "COVID_VACCINE/vaccine_dict.json"
PATH_codon_to_protein = "COVID_VACCINE/codon_to_protein.json"

def read_fasta(file_name):
    # Read fasta file
    return "".join(open(file_name, "r").read().split("\n")[1:])

# Open COVID spike protein file and codon map
codonMap = json.loads(open(PATH_codon_map, "r").read())
codonProtein = json.loads(open(PATH_codon_to_protein, "r").read())

def conv_to_protein(seq):
    s = ""
    for i in range(0, len(seq), 3):
        s += codonProtein[seq[i:i+3]]
    return s

# Optimize virus for vaccine given codon map
def codon_optimize(spike):
    newVaccine = ""
    # Now circulate through the codons, reading the nucleotide bases 3 at a time.
    for i in range(0, len(spike), 3):
        # Match the spike codon to the corresponding vaccine codon.
        newVaccine += codonMap.get(spike[i:i+3], spike[i:i+3])
    return newVaccine

def main(argv):
    # Read input sequence file
    PATH_CoV = FLAGS.file + ".fasta"
    spikeF = read_fasta(PATH_CoV)

    # Read comparison file
    if FLAGS.compare:
        PATH_vaccine = FLAGS.debug
        actual_vaccineF = read_fasta(PATH_vaccine)

    codon_op_output = codon_optimize(spikeF)
    print("\n\nNUCLEOTIDE SEQUENCE\n-------------------------")
    print(codon_op_output)
    # Write to file FLAGS.output
    wr = open(FLAGS.file + "_Pred.fasta", "w")
    wr.write(F">CodonMap{round(time.time())}\n") # Title: CodonMap{HASH}
    wr.write("\n".join([codon_op_output[i:i+50] for i in range(0, len(codon_op_output), 50)]))
    wr.close()
    print(F"Successfully wrote to {FLAGS.file}_Pred.fasta")
    
    if FLAGS.compare:
        # Compare the two using simple_compare
        comp = SequenceComp(codon_op_output, actual_vaccineF)
        comp.print_compare(codonProtein)
    else:
        # Print out the amino acid sequence
        print("\nAMINO ACID SEQUENCE\n----------------------------------")
        out = conv_to_protein(spikeF)
        print(out)
        # Write to file FLAGS.output
        wr = open(FLAGS.file + "_Peptide.fasta", "w")
        wr.write(F">Peptides{round(time.time())}\n") # Title: Peptides{HASH}
        wr.write("\n".join([out[i:i+50] for i in range(0, len(out), 50)]))
        wr.close()
        print(F"Successfully wrote to {FLAGS.file}_Peptide.fasta")


if __name__ == '__main__':
  app.run(main)