import re
import sys
from random import random
from math import log
from collections import defaultdict


class Trigram():

    # Gets file from argument
    infile = sys.argv[1]
    language = sys.argv[1][-2:]

    # Counts trigrams in input
    tri_counts = defaultdict(int)
    bi_counts = defaultdict(int)

    # Task 1
    # Removes special characters
    # Converts all digits to 0
    # Sets strings to be all lowercase
    def preprocess_line(self, line):
        line = re.sub(r'[1-9]', '0', line)
        line = re.sub(r'[^a-z0.\s]', '', line.lower())
        line = '#' + line[:-2] + '#'
        return line

    # This bit of code gives an example of how you might extract trigram counts
    # from a file, line by line. If you plan to use or modify this code,
    # please ensure you understand what it is actually doing, especially at the
    # beginning and end of each line. Depending on how you write the rest of
    # your program, you may need to modify this code.
    def extractTrigram(self):
        print("Extracting trigrams")
        with open(self.infile) as f:
            for line in f:
                line = self.preprocess_line(line)
                for j in range(len(line)-(3)):
                    trigram = line[j:j+3]
                    self.tri_counts[trigram] += 1

    def extractBigram(self):
        print("Extracting bigrams")
        with open(self.infile) as f:
            for line in f:
                line = self.preprocess_line(line)
                for j in range(len(line)-(2)):
                    bigram = line[j:j+2]
                    self.bi_counts[bigram] += 1

    def extractNgram(self, ncounts, n):
        print("Extracting Ngrams where N = ", n)
        with open(self.infile) as f:
            for line in f:
                line = self.preprocess_line(line)
                for j in range(len(line)-(n)):
                    ncounts[line[j:j+2]] += 1

    # Some example code that prints out the counts. For small input files
    # the counts are easy to look at but for larger files you can redirect
    # to an output file (see Lab 1).

    def printTrigram(self):
        print("Generating trigram model from ",
              self.infile, ", sorted alphabetically:")
        with open('../assignment1-data/alphabetical_trigram.' + self.language, 'w') as f:
            for trigram in sorted(self.tri_counts.keys()):
                print(trigram, " ",
                      '{:.2e}'.format(self.tri_counts[trigram] / self.bi_counts[trigram[:-1]]), file=f)
        print("Generating trigram model from ",
              self.infile, ", sorted numerically:")
        with open('../assignment1-data/numerical_trigram.' + self.language, 'w') as f:
            for tri_count in sorted(self.tri_counts.items(), key=lambda x: x[1], reverse=True):
                print(tri_count[0], " ", str(
                    '{:.2e}'.format(tri_count[1] / self.bi_counts[tri_count[0][:-1]])), file=f)

    def parseModel(self, modelFile):
        model = {}
        file = open(modelFile, 'r')
        for line in file:
            splitLine = line.split()
            if(len(splitLine) == 2):
                model[splitLine[0]] = splitLine[1]
            else:
                model['   '] = splitLine[0]
        return model

    # Task 4
    # Generates output string based on language model
    def generate_from_LM(self, model):
        model = self.parseModel(model)
        phrase = 'th'
        for i in range(298):
            rand = random()
            total = 0
            for tri, prob in model.items():
                if(phrase[-2:] in tri):
                    total += float(prob)
                    if(rand < total):
                        phrase += tri[-1:]
                        break
        return phrase


def main():

    # Check if number of arguments are correct
    if len(sys.argv) != 2:
        print("Usage: ", sys.argv[0], "<training_file>")
        sys.exit(1)

    Trigram().extractBigram()
    Trigram().extractTrigram()
    # Trigram().extractNgram(Trigram().bi_counts, 2)
    # Trigram().extractNgram(Trigram().tri_counts, 3)
    Trigram().printTrigram()

    print('\nGenerated output from our generated model:\n')
    print(Trigram().generate_from_LM(
        '../assignment1-data/alphabetical_trigram.en'))

    print('\nGenerated output from example model-br.en:\n')
    print(Trigram().generate_from_LM('../assignment1-data/model-br.en'))


if __name__ == "__main__":
    main()
