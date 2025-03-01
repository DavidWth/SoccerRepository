import unittest
import sys
import os
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../../src/analysis'))

from src.analysis.LoadJSONFile import load_JSON_file

class LoadJSONFileTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_JSON_file(self):
        load_JSON_file()


if __name__ == '__main__':
    unittest.main()