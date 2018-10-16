import unittest
import Assignment_1 as tr


class TestMethods(unittest.TestCase):

    def testPreprocessor(self):
        print(tr.Trigram().preprocess_line("Ich möchte 1 Bier."))

if __name__ == '__main__':
    unittest.main()
