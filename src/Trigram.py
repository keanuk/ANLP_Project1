import re
import sys
import random
from math import log
from itertools import product
from collections import defaultdict


class Trigram():

    # Gets file from argument
    infile = sys.argv[1]
    language = sys.argv[1][-2:]

    possible_characters = ' #.0abcdefghijklmnopqrstuvwxyz'

    # Counts trigrams in input
    tri_counts = dict.fromkeys([''.join(i) for i in product(possible_characters, repeat=3)], 0)
    bi_counts = dict.fromkeys([''.join(i) for i in product(possible_characters, repeat=2)], 0)

    # Task 1
    # Removes special characters
    # Converts all digits to 0
    # Sets strings to be all lowercase
    def preprocess_line(self, line):
        line = re.sub(r'[1-9]', '0', line)
        line = re.sub(r'[^a-z0.\s]', '', line.lower())
        line = '#' + line[:-1] + '#'
        return line

    def generateAllNgrams(self, n):
        return 

    # Extracts Ngrams from given training file
    def extractNgram(self, ncounts, n):
        with open(self.infile) as f:
            for line in f:
                line = self.preprocess_line(line)
                for j in range(len(line)-(n)):
                    ncounts[line[j:j+n]] += 1

    def printTrigram(self):
        with open('../assignment1-data/alphabetical_trigram.' + self.language, 'w') as f:
            for trigram in sorted(self.tri_counts.keys()):
                print(trigram, " ", '{:.2e}'.format((self.tri_counts[trigram] + 1) / (self.bi_counts[trigram[:-1]] + len(self.bi_counts))), file=f)
        # print("Generating trigram model from ", self.infile, ", sorted numerically:")
        # with open('../assignment1-data/numerical_trigram.' + self.language, 'w') as f:
        #     for tri_count in sorted(self.tri_counts.items(), key=lambda x: x[1], reverse=True):
        #         if(tri_count[1] != 0):
        #             print(tri_count[0], " ", str('{:.2e}'.format(tri_count[1] / self.bi_counts[tri_count[0][:-1]])), file=f)

    def splitAtFirstDigit(self, line):
        for char in line:
            if char.isdigit():
                if int(char) > 0:
                    result = line.split(char, 1)
                    result[0] = re.sub(r'[\n\t]', '', result[0][:3])
                    result[1] = re.sub(r'[\n\t]', '', result[1])
                    return [result[0], char + result[1]]

    def parseModel(self, modelFile):
        model = {}
        file = open(modelFile, 'r')
        for line in file:
            splitLine = self.splitAtFirstDigit(line)
            model[splitLine[0]] = splitLine[1]
        return model

    # Task 4
    # Generates output string based on language model
    def generate_from_LM(self, model):
        model = self.parseModel(model)
        phrase = random.choice(list(model.keys())[:2])
        for i in range(298):
            rand = random.random()
            total = 0
            # print("Random: ", rand)
            for tri, prob in model.items():
                if(phrase[-2:] == tri[:2]):
                    total += float(prob)
                    # print("Total: ", total)
                    if(rand < total):
                        # print("\nUSED CHARACTER: ", tri[-1:], "\n")
                        phrase += tri[-1:]
                        break
        return phrase


def main():

    # Check if number of arguments are correct
    if len(sys.argv) != 2:
        print("Usage: ", sys.argv[0], "<training_file>")
        sys.exit(1)

    Trigram().extractNgram(Trigram().bi_counts, 2)
    Trigram().extractNgram(Trigram().tri_counts, 3)
    Trigram().printTrigram()

    print('\nGenerated output from our generated model:\n')
    print(Trigram().generate_from_LM('../assignment1-data/alphabetical_trigram.en'))

    print('\nGenerated output from example model-br.en:\n')
    print(Trigram().generate_from_LM('../assignment1-data/model-br.en'))


if __name__ == "__main__":
    main()
