import unittest
from src.filter import word_search, word_search_strict

class TestFilter(unittest.TestCase):
    def test_word_search(self):
        description = ["This is a test", "Another sentence", "And another one Yes"]
        words = ["test", "missing"]
        self.assertTrue(word_search(description, words))

        words = ["missing"]
        self.assertFalse(word_search(description, words))

    def test_word_search_strict(self):
        description = ["This is a test", "Another sentence", "And another one Yes"]
        words = ["test", "another"]
        self.assertTrue(word_search_strict(description, words))

        words = ["test", "missing"]
        self.assertFalse(word_search_strict(description, words))

if __name__ == '__main__':
    unittest.main()
