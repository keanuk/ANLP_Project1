import re
import sys
from random import random
from math import log
from collections import defaultdict


class Trigram():

    # Check if number of arguments are correct
    if len(sys.argv) != 2:
        print("Usage: ", sys.argv[0], "<training_file>")
        sys.exit(1)

    # Gets file from argument
    infile = sys.argv[1]

    # Counts trigrams in input
    tri_counts = defaultdict(int)

    # Task 1
    # Removes special characters
    # Converts all digits to 0
    # Sets strings to be all lowercase
    def preprocess_line(self, line):
        line = re.sub(r'[1-9]', '0', line)
        line = re.sub(r'[^a-z0.\s]', '', line.lower())
        return line

    # This bit of code gives an example of how you might extract trigram counts
    # from a file, line by line. If you plan to use or modify this code,
    # please ensure you understand what it is actually doing, especially at the
    # beginning and end of each line. Depending on how you write the rest of
    # your program, you may need to modify this code.
    def extractTrigram(self):
        with open(self.infile) as f:
            for line in f:
                line = self.preprocess_line(line)
                for j in range(len(line)-(3)):
                    trigram = line[j:j+3]
                    self.tri_counts[trigram] += 1

    # Some example code that prints out the counts. For small input files
    # the counts are easy to look at but for larger files you can redirect
    # to an output file (see Lab 1).
    def printTrigram(self):
        print("Trigram counts in ", self.infile, ", sorted alphabetically:")
        with open('alphabetical_trigram.txt', 'w') as f:
            for trigram in sorted(self.tri_counts.keys()):
                # print(trigram, ": ", self.tri_counts[trigram])
                print(trigram, ": ", self.tri_counts[trigram], file=f)
        print("Trigram counts in ", self.infile, ", sorted numerically:")
        with open('numerical_trigram.txt', 'w') as f:
            for tri_count in sorted(self.tri_counts.items(), key=lambda x: x[1], reverse=True):
                # print(tri_count[0], ": ", str(tri_count[1]))
                print(tri_count[0], ": ", str(tri_count[1]), file=f)

    # Task 4
    # Generates output string based on language model
    def generate_from_LM(self, model):
        return ''


def main():
    Trigram().extractTrigram()
    Trigram().printTrigram()


if __name__ == "__main__":
    main()
