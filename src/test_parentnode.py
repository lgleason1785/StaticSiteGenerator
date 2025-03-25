import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode("b", "child")
        node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_chidlren(self):
        node = ParentNode("b", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_props(self):
        child_node = LeafNode("b", "child")
        node = ParentNode("a", [child_node], {"href": "https://www.google.com"})
        test_str = '<a href="https://www.google.com"><b>child</b></a>'
        self.assertEqual(node.to_html(), test_str)
    
    def test_to_html_with_empty_children(self):
        node = ParentNode("h1", [])
        self.assertEqual(node.to_html(), "<h1></h1>")
    
    def test_to_html_multiple_children(self):
        child1 = LeafNode("b", "child1")
        child2 = LeafNode("h1", "child2")
        node = ParentNode("div", [child1, child2])
        test_str = "<div><b>child1</b><h1>child2</h1></div>"
        self.assertEqual(node.to_html(), test_str)
    
    def test_to_html_complex_nesting(self):
        leaf1 = LeafNode("div", "leaf1")
        leaf2 = LeafNode("b", "leaf2")
        inner_parent = ParentNode("b", [leaf1, leaf2])
        leaf3 = LeafNode("p", "leaf3")
        node = ParentNode("b", [inner_parent, leaf3])
        test_str = "<b><b><div>leaf1</div><b>leaf2</b></b><p>leaf3</p></b>"
        self.assertEqual(node.to_html(), test_str)

    def test_multiple_props(self):
        child_node = LeafNode("span", "child")
        props = {
            "class": "container",
            "id": "main",
            "data-test": "test-div"
        }
        node = ParentNode("div", [child_node], props)
        # The order of props might vary, so we'll check parts of the string
        html = node.to_html()
        self.assertTrue(html.startswith("<div "))
        self.assertTrue(html.endswith("><span>child</span></div>"))
        self.assertTrue('class="container"' in html)
        self.assertTrue('id="main"' in html)
        self.assertTrue('data-test="test-div"' in html)