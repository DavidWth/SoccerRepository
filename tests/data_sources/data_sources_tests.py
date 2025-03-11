import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/'))
from data_sources import file_loader
import pandas as pd

class DataSourcesTest(unittest.TestCase):
    def setUp(self):
        self.KICKER_FILE='D:\\DevOps\\python_work\\venv\\demoenv\\resources\\output_k.json'
        self.addClassCleanupTF_FILE='D:\\DevOps\\python_work\\venv\\demoenv\\resources\\output_tf.json'
        self.FIFA_FILE='D:\\DevOps\\python_work\\venv\\demoenv\\resources\\players_fifa.json'

    def tearDown(self):
        pass

    def test_load_JSON_into_data_frame_file(self):
        data = file_loader.load_json_file_into_dataframe(self.KICKER_FILE)

        self.assertIsInstance(data, pd.DataFrame)
        self.assertGreater(len(data), 0)

    def test_load_JSON_into_data_frame_file_not_existing(self):
        data = file_loader.load_json_file_into_dataframe("xxx.json")

        self.assertEqual(data, [])
    
