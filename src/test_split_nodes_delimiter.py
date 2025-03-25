import unittest

from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

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

    