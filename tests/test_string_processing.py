import unittest
from src.string_processing import split_sentences

class TestStringProcessing(unittest.TestCase):
    def test_split_sentences(self):
        description = "This is a test. Another sentence! And another one:Yes."
        expected_output = [
            "This is a test",
            "Another sentence",
            "And another one Yes"
        ]
        self.assertEqual(split_sentences(description), expected_output)

    def test_split_sentences_with_special_characters(self):
        description = "This is a test! Show more. Another sentence:Show less."
        expected_output = [
            "This is a test",
            "Another sentence"
        ]
        self.assertEqual(split_sentences(description), expected_output)

    def test_split_sentences_with_newlines(self):
        description = "This is a test.\nAnother sentence.\nShow more."
        expected_output = [
            "This is a test",
            "Another sentence"
        ]
        self.assertEqual(split_sentences(description), expected_output)

if __name__ == '__main__':
    unittest.main()
