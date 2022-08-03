import unittest
import json
from justry import Scraper
from postgres import write_to_db, read_from_db


class TestScraper(unittest.TestCase): #TestCase will allow to access a lot of testing capabilities within this class.
    
    def test_create_json(self):
        dicti = {'a': 1, 'b': 2}
        webscraper = Scraper()
        webscraper.create_json(dicti, 'test.json')

        new_var = json.load(open('data/json/test.json'))
        self.assertDictEqual(dicti, new_var)


class TestIntegrationScraper(unittest.TestCase):

    def test_scraping(self):
        webscraper = Scraper()
        webscraper.fetch_community('gaming')
        new_var = json.load(open('data/json/gaming.json'))
        self.assertEqual(type(new_var), dict)
        self.assertGreater(len(new_var), 1)
        self.assertSetEqual(set(list(new_var.values())[0].keys()), {'Title', 'Comment', 'ImageSource', 'ID', 'Vote', 'Body'})


class TestIntegrationDB(unittest.TestCase):

    def test_write_to_db(self):
        datadict = {'a': {'x': 1, 'y': 2}, 'b': {'x': 4, 'y': 8}}
        community_name = 'test'
        write_to_db(datadict, community_name) 
        db_df = read_from_db(community_name)
        self.assertListEqual(db_df['index'].to_list(), list(datadict.keys()))
        self.assertListEqual(db_df[['x', 'y']].to_dict(orient= 'records'), list(datadict.values()))
