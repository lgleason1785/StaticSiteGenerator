import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a test")
        node2 = HTMLNode("p", "This is a test")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = HTMLNode("p", "This is a test")
        node2 = HTMLNode("a", "This is a test")
        self.assertNotEqual(node, node2)

        node3 = HTMLNode("p", "This is another test")
        self.assertNotEqual(node, node3)

        node4 = HTMLNode("p", "This is a test", None, {"class": "example"})
        self.assertNotEqual(node, node4)

    def test_props_to_html(self):
        node = HTMLNode("h1", "", None, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

        
    def test_props_to_html_with_empty_props(self):
        node = HTMLNode("h1", "", None, {})
        self.assertEqual("", node.props_to_html())

    def test_props_to_html_with_none_props(self):
        node = HTMLNode("h1", "", None, None)
        self.assertEqual("", node.props_to_html())

    def test_repr(self):
        node = HTMLNode("p", "This is a test")
        repr_check = 'HTMLNode(tag="p", value="This is a test", children=None, props=None)'
        self.assertEqual(node.__repr__(), repr_check)