import re
import sys
import random
import numpy as np
from math import log2
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
        line = re.sub('[1-9]', '0', line)
        line = re.sub('[^a-z0.\s]', '', line.lower())
        line = '##' + line[:-1] + '#'
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
                print(trigram, " ", '{:.2e}'.format((self.tri_counts[trigram] + 1) / (self.bi_counts[trigram[:-1]] + len(self.possible_characters))), file=f)
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
                    result[0] = re.sub('[\n\t]', '', result[0][:3])
                    result[1] = re.sub('[\n\t]', '', result[1])
                    return [result[0], char + result[1]]

    def parseModel(self, modelFile):
        model = {}
        file = open(modelFile, 'r')
        for line in file:
            splitLine = self.splitAtFirstDigit(line)
            model[splitLine[0]] = float(splitLine[1])
        return model

    # Task 4
    # Generates output string based on language model
    def generate_from_LM(self, model):
        model = self.parseModel(model)
        phrase = '##'
        for i in range(298):
            filteredModel = {key : value for (key, value) in model.items() if phrase[-2:] == key[:2]}
            phrase += str(np.random.choice(list(filteredModel.keys()), 1, p=[float(i)/sum(list(filteredModel.values())) for i in list(filteredModel.values())]))[4:5]
            if(phrase[-1:] == '#'):
                phrase += '#'
                i += 1
        phrase = phrase.replace('##', '\n')
        return re.sub(r'[#]', '', phrase)

    # Task 5
    # Calculate perplexity
    def getPerplexity(self, model, testDoc):
        testString = ''
        model = self.parseModel(model)
        triSum = 0
        testString = ''
        with open(testDoc) as f:
            for line in f:
                pline = self.preprocess_line(line)
                testString += pline
                triCount = len(pline) - 3
                for i in range(triCount):
                    triSum += log2(model[pline[:3]])
                    pline = pline[1:]
        perplexity = -1 / len(testString) * triSum
        print("Perplexity is: ", perplexity)
        print("Sum of all trigram probabilities: ", triSum)


def main():

    # Check if number of arguments are correct
    if len(sys.argv) != 2:
        print("Usage: ", sys.argv[0], "<training_file>")
        sys.exit(1)

    Trigram().extractNgram(Trigram().bi_counts, 2)
    Trigram().extractNgram(Trigram().tri_counts, 3)
    Trigram().printTrigram()

    print('\n**********Generated output from example model-br.en:')
    print(Trigram().generate_from_LM('../assignment1-data/model-br.en'))

    print('\n**********Generated output from our generated model:')
    print(Trigram().generate_from_LM('../assignment1-data/alphabetical_trigram.en'))

    print("\n**********Calculating perplexity of the document with given model:")
    print(Trigram().getPerplexity('../assignment1-data/model-br.en', '../assignment1-data/test'))

    print("\n**********Calculating perplexity of the document with english model:")
    print(Trigram().getPerplexity('../assignment1-data/alphabetical_trigram.en', '../assignment1-data/test'))

    print("\n**********Calculating perplexity of the document with german model:")
    print(Trigram().getPerplexity('../assignment1-data/alphabetical_trigram.de', '../assignment1-data/test'))

    print("\n**********Calculating perplexity of the document with spanish model:")
    print(Trigram().getPerplexity('../assignment1-data/alphabetical_trigram.es', '../assignment1-data/test'))


if __name__ == "__main__":
    main()
