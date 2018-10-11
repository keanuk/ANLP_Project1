import unittest
import Trigram as tr


class TestMethods(unittest.TestCase):

    def testPreprocessor(self):
        print(tr.Trigram().preprocess_line("Ich möchte 1 Bier."))

    def testTrigramGeneration(self):
        print(tr.Trigram().generateAllNgrams(3))

if __name__ == '__main__':
    unittest.main()
