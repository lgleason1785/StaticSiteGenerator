import unittest

from enums import TextType
from textnode import TextNode
from helper_functions import text_node_to_html_node

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic_text(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code_text(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")
    
    def test_link_text(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.testimage.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.testimage.com"})

    def test_image_text(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.test.com", "alt": "This is an image"})

    def test_invalid_text_type(self): 
        node = TextNode("This is an error", "hyper")
        with self.assertRaises(TypeError):
            text_node_to_html_node(node)

    def test_no_value_text_node(self):
        node = TextNode(None, TextType.BOLD)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_empty_text_node(self):
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")


    def test_link_node_missing_href(self):
        node = TextNode("This is a link", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_node_missing_src_and_alt(self):
        node = TextNode(None, TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)