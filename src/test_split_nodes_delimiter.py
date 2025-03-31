import unittest

from helper_functions import split_nodes_delimiter
from textnode import TextNode
from enums import TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        node = TextNode("This is a `test` node", TextType.TEXT)
        expected_result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("test", TextType.CODE),
            TextNode(" node", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected_result)

    def test_multiple_delimiter_pair(self):
        node = TextNode("This is a **test** node", TextType.TEXT)
        expected_result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("test", TextType.BOLD),
            TextNode(" node", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected_result)

    def test_unmatched_delimiters(self):
        node = TextNode("This is an **unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    
    def test_no_delimiters_present(self):
        node = TextNode("This is plain text", TextType.TEXT)
        expected_result = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected_result)

    def test_multiple_delimiters(self):
        node = TextNode("This is **bold** and another **bold** here", TextType.TEXT)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and another ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected_result)

    def test_empty_strings_between_delimiter(self):
        node = TextNode("This has **bold** and an empty **** delimiter", TextType.TEXT)
        expected_result = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and an empty ", TextType.TEXT),
            TextNode(" delimiter", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected_result)