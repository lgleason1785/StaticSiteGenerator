import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

if __name__ == "__main__":
    unittest.main()