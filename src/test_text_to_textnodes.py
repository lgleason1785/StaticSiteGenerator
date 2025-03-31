import unittest

from enums import TextType
from textnode import TextNode
from helper_functions import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text_to_textnode(self):
        text = "This is plain text"
        expected_result = [TextNode("This is plain text", TextType.TEXT)]
        self.assertListEqual(text_to_textnodes(text), expected_result)

    def test_bold_to_textnode(self):
        text = "This is **bold** text"
        text2 = "This is an **error"
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertListEqual(text_to_textnodes(text), expected_result)
        with self.assertRaises(ValueError):
            text_to_textnodes(text2)

    def test_italic_to_textnode(self):
        text = "This is _italic_ text"
        text2 = "This is an _error"
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertListEqual(text_to_textnodes(text), expected_result)
        with self.assertRaises(ValueError):
            text_to_textnodes(text2)

    
    def test_code_to_textnode(self):
        text = "This is `code`"
        text2 = "This is an `error"
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        self.assertListEqual(text_to_textnodes(text), expected_result)
        with self.assertRaises(ValueError):
            text_to_textnodes(text2)

    def test_mixed_markdown_emphasis(self):
        text = "This is a test with **bold text** and _italic text_ and `code`"
        expected_result = [
            TextNode("This is a test with ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        self.assertListEqual(text_to_textnodes(text), expected_result)

    def test_markdown_link_to_textnode(self):
        text = "This text contains a [link](https://example.com) and not much else"
        expected_result = [
            TextNode("This text contains a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and not much else", TextType.TEXT)
        ]
        self.assertListEqual(text_to_textnodes(text), expected_result)
    
    def test_markdown_image_to_textnode(self):
        text = "This text contains an ![image](https://example.com/test.jpg) and not much else"
        expected_result = [
            TextNode("This text contains an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/test.jpg"),
            TextNode(" and not much else", TextType.TEXT)
        ]
        self.assertListEqual(text_to_textnodes(text), expected_result)

    def test_mixed_markdown_emphasis_with_link_and_image(self):
        text = "This is a text that has **bold text** an ![image](https://example.com/test.jpg), some _italics_, and a [link](https://example.com)"
        expected_result = [
            TextNode("This is a text that has ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/test.jpg"),
            TextNode(", some ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
            TextNode(", and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com")
        ]
        self.assertListEqual(text_to_textnodes(text), expected_result)
