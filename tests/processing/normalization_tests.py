import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src'))

from processing import normalization

class NormalizationTests(unittest.TestCase):
    def setUp(self):
        self.test_cases = [
            ("Mathys", "Angély", "mathys_angely"),
            ("Filippo", "Mané", "filippo_mane"),  # Stripping spaces
            ("Alexis", "Claude-Maurice", "alexis_claude-maurice"),  # Special characters
            ("Mahmut", "Kücüksahin", "mahmut_kucuksahin"),  # Apostrophe case
            ("Issa", "Kaboré", "issa_kabore"),  # Mixed case handling
            ("Eric", "Oelschlägel", "eric_oelschlagel"),  # Mixed case handling
            ("Leo", "Østigård", "leo_ostigard"),  # Mixed case handling
            ("Jérôme", "Roussillon", "jerome_roussillon"),  # Mixed case handling
            ("László", "Bénes", "laszlo_benes"),  # Mixed case handling
            ("Leo", "Åndalsness", "leo_andalsness"),  # Mixed case handling
           # ("Adam", "Dźwigała", "adam_dzwigala"),  # Mixed case handling
        ]


    def tearDown(self):
        pass

    def test_normalize_names_with_first_last_name(self):
        for first_name, last_name, expected in self.test_cases:
            with self.subTest(first_name=first_name, last_name=last_name):
                result = normalization.normalize_name(first_name, last_name)
                self.assertEqual(result, expected)
        
    def test_normalize_names_with_empty_params(self):
        normalized_name = normalization.normalize_name("", "")
        
        self.assertIsInstance(normalized_name, str)


