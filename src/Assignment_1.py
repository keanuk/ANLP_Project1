import re
import sys
import numpy as np
from math import log2
from itertools import product

class Trigram():

    # Gets file from argument
    infile = sys.argv[1]
    language = sys.argv[1][-2:]

    # String containing all possible characters found in our trigrams
    possible_characters = ' #.0abcdefghijklmnopqrstuvwxyz'

    # Counts trigrams in input
    tri_counts = dict.fromkeys([''.join(i) for i in product(possible_characters, repeat=3)], 0)
    bi_counts = dict.fromkeys([''.join(i) for i in product(possible_characters, repeat=2)], 0)

    # Removes trigrams that should not ever occur from the trigram dictionary
    def cleanTri(self):
        for key in list(self.tri_counts.keys()):
            if key[-2:] == "##":
                del self.tri_counts[key]
            if key[0] != '#' and key[1] == '#' and key[2] != '#':
                del self.tri_counts[key]



    ### Task 1 ###

    # Removes special characters
    # Converts all digits to 0
    # Sets strings to be all lowercase
    def preprocess_line(self, line):
        line = re.sub('[1-9]', '0', line)
        line = re.sub('[^a-z0.\s]', '', line.lower())
        line = '##' + line[:-1] + '#'
        return line



    ### Task 3 ###

    # Extracts Ngrams from given training file and counts thier occurances
    def extractNgram(self, ncounts, n):
        with open(self.infile) as f:
            for line in f:
                line = self.preprocess_line(line)
                for j in range(len(line)-(n - 1)):
                    ncounts[line[j:j+n]] += 1

    # Calculates trigram probabilities and smoothes them using add-1 smoothing
    def printTrigram(self):
        with open('../assignment1-data/alphabetical_trigram.' + self.language, 'w') as f:
            for trigram in sorted(self.tri_counts.keys()):
                print(trigram, " ", '{:.2e}'.format(((self.tri_counts[trigram]) + 1) / (self.bi_counts[trigram[:-1]] + len(self.possible_characters))), file=f)
        with open('../assignment1-data/numerical_trigram.' + self.language, 'w') as f:
            for tri_count in sorted(self.tri_counts.items(), key=lambda x: x[1], reverse=True):
                print(tri_count[0], " ", str('{:.2e}'.format((tri_count[1] + 1) / (self.bi_counts[tri_count[0][:-1]] + len(self.possible_characters)))), file=f)



    ### Task 4 ###

    # Splits string when first nonzero digit occurs to parse the model trigrams and probabilities
    def splitAtFirstDigit(self, line):
        for char in line:
            if char.isdigit():
                if int(char) > 0:
                    result = line.split(char, 1)
                    result[0] = re.sub('[\n\t]', '', result[0][:3])
                    result[1] = re.sub('[\n\t]', '', result[1])
                    return [result[0], char + result[1]]

    # Parses models from text document and stores them in dictionary to be used for string generation
    def parseModel(self, modelFile):
        model = {}
        file = open(modelFile, 'r')
        for line in file:
            splitLine = self.splitAtFirstDigit(line)
            model[splitLine[0]] = float(splitLine[1])
        return model

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



    ### Task 5 ###

    # Calculate perplexity
    def getPerplexity(self, model, testDoc):
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
        entropy = -1 / len(testString) * triSum
        perplexity = 2 ** entropy
        return perplexity



    ### Task 6 ###

    # Counts consonant clusters in a language
    # Function checks for clusters longer than 4 and if they occur more than 4 times
    # Long consonant clusters are very common in german, especially our preprocessed strings which remove special characters
    def getConsonantClusters(self, testString):
        isGerman = False
        cClusters = re.findall(r'(?:(?![aeiouy])[a-z]){2,}', testString)
        longClusters = [c for c in cClusters if len(c) > 4]
        print("The longest consonant cluster is ", max(cClusters, key=len), "\n", longClusters)
        if len(max(cClusters, key=len)) > 4 and len(longClusters) > 4:
            isGerman = True
        return isGerman

    # Checks for occurances of s-consonants at the start of a word
    # This combination is very uncommon in spanish
    def getSConsonant(self, testString):
        isSpanish = False
        sConsonants = re.findall(r'\ss[b-df-hj-np-tv-xz]', testString)
        print('There are ', len(sConsonants), ' occurances of s-consonants at the start of a word.')
        if len(sConsonants) < 1:
            isSpanish = True
        return isSpanish

    # Checks for language specific quirks to determine the likelihood that a text document belongs to a specific language
    def checkLangRules(self, testDoc):
        testString = ''
        with open(testDoc) as f:
            for line in f:
                pline = self.preprocess_line(line)
                testString += pline
        isGerman = self.getConsonantClusters(testString)
        isSpanish = self.getSConsonant(testString)
        if isGerman == True:
            print("The document is probably German.")
        else:
            print("The document is probably not German.")
        if isSpanish == True:
            print("The document is probably Spanish.")
        else: 
            print("The document is probably not Spanish.")
        if isGerman == False and isSpanish == False:
            print("The document is probably English.")

def main():

    # Check if number of arguments are correct
    if len(sys.argv) != 2:
        print("Usage: ", sys.argv[0], "<training_file>")
        sys.exit(1)

    # Task 1 and Task 3
    Trigram().cleanTri()
    Trigram().extractNgram(Trigram().bi_counts, 2)
    Trigram().extractNgram(Trigram().tri_counts, 3)
    Trigram().printTrigram()

    # Task 4
    print('\n**********Generated output from example model-br.en:')
    print(Trigram().generate_from_LM('../assignment1-data/model-br.en'))

    print('\n**********Generated output from our generated model:')
    print(Trigram().generate_from_LM('../assignment1-data/alphabetical_trigram.en'))

    # Task 5
    print("\n**********Calculating perplexity of the document with given model:")
    print(Trigram().getPerplexity('../assignment1-data/model-br.en', '../assignment1-data/test'))

    print("\n**********Calculating perplexity of the document with english model:")
    print(Trigram().getPerplexity('../assignment1-data/alphabetical_trigram.en', '../assignment1-data/test'))

    print("\n**********Calculating perplexity of the document with german model:")
    print(Trigram().getPerplexity('../assignment1-data/alphabetical_trigram.de', '../assignment1-data/test'))

    print("\n**********Calculating perplexity of the document with spanish model:")
    print(Trigram().getPerplexity('../assignment1-data/alphabetical_trigram.es', '../assignment1-data/test'))

    # Task 6
    print("\n**********Language specific rules:")
    Trigram().checkLangRules('../assignment1-data/test')


if __name__ == "__main__":
    main()
