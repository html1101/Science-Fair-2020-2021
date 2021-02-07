"""
Simple script to convert .gb to .fasta and push into a file.
"""
from Bio import SeqIO
from absl import flags
from absl import app

FLAGS = flags.FLAGS

flags.DEFINE_string("file", "COVID_VACCINE/SARS-CoV.gb", "The file to convert.")
flags.DEFINE_string("typefrom", "genbank", "Type of script to input.")
flags.DEFINE_string("typeto", "fasta", "Type of script to convert to.")

def main(_argv):
    # Read input sequence file
    if FLAGS.file and FLAGS.typefrom and FLAGS.typeto:
        conv = SeqIO.read(FLAGS.file, FLAGS.typefrom)
        fileN = "".join(FLAGS.file.split(".")[:-1]) + "." + FLAGS.typeto # Filename
        SeqIO.write([conv], fileN, FLAGS.typeto)
        print(F"Successfully wrote to {fileN}")


if __name__ == "__main__":
    app.run(main)