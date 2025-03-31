import unittest

from enums import TextType
from textnode import TextNode
from helper_functions import split_nodes_link

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        old_nodes = [TextNode("This is a [link](https://example.com) and not much else", TextType.TEXT)]
        expected_result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and not much else", TextType.TEXT)
        ]
        self.assertListEqual(split_nodes_link(old_nodes), expected_result)

    def test_multiple_links(self):
        old_nodes = [TextNode("This is the [first](https://example.com/1) and the [second](https://example.com/2) link", TextType.TEXT)]
        expected_results = [
            TextNode("This is the ", TextType.TEXT),
            TextNode("first", TextType.LINK, "https://example.com/1"),
            TextNode(" and the ", TextType.TEXT),
            TextNode("second", TextType.LINK, "https://example.com/2"),
            TextNode(" link", TextType.TEXT)
        ]
        self.assertListEqual(split_nodes_link(old_nodes), expected_results)

    def test_multiple_nodes_with_links(self):
        old_nodes = [
            TextNode("This is the [first](https://example.com/1) and the [second](https://example.com/2) link", TextType.TEXT),
            TextNode("This is a [link](https://example.com/test)", TextType.TEXT)
            ]
        expected_results = [
            TextNode("This is the ", TextType.TEXT),
            TextNode("first", TextType.LINK, "https://example.com/1"),
            TextNode(" and the ", TextType.TEXT),
            TextNode("second", TextType.LINK, "https://example.com/2"),
            TextNode(" link", TextType.TEXT),
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com/test")
        ]
        self.assertListEqual(split_nodes_link(old_nodes), expected_results)

    def test_multiple_nodes_mixed_content(self):
        old_nodes = [
            TextNode("This is the ![first](https://example.com/1.jpg) and the ![second](https://example.com/2.jpg) image", TextType.TEXT),
            TextNode("This is an ![image](https://example.com/test.jpg)", TextType.TEXT),
            TextNode("This is a [link](https://example.com)", TextType.TEXT),
            TextNode("Click Me!", TextType.LINK, "https://example.com/test.sh"),
            TextNode("Dog pics", TextType.IMAGE, "https://example.com/dog.jpg")
            ]
        expected_results = [
            TextNode("This is the ![first](https://example.com/1.jpg) and the ![second](https://example.com/2.jpg) image", TextType.TEXT),
            TextNode("This is an ![image](https://example.com/test.jpg)", TextType.TEXT),
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("Click Me!", TextType.LINK, "https://example.com/test.sh"),
            TextNode("Dog pics", TextType.IMAGE, "https://example.com/dog.jpg")
        ]
        self.assertListEqual(split_nodes_link(old_nodes), expected_results)