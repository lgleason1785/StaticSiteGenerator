import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is bold text")
        self.assertEqual(node.to_html(), "<b>This is bold text</b>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "This is a div")
        self.assertEqual(node.to_html(), "<div>This is a div</div>")

    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Click me", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me</a>')
    
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Text here")
        self.assertEqual(node.to_html(), "Text here")
    
    def leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()