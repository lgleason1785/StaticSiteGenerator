import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_links,
    extract_markdown_images
)

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
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected_result)\
        
class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_link(self):
        text = "This a [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_multiple_links(self):
        text = "This is the [first](https://example.com/1) link and the [second](https://example.com/2)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("first", "https://example.com/1"), ("second", "https://example.com/2")], matches)
        
    def test_no_links(self):
        text = "Plain text"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_no_anchor_text(self):
        text = "This link has no anchor text [](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)

    def test_only_images(self):
        text = "Omnly images here ![image](https://i.imgur.com/xyz)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_complex_urls(self):
        text = "[complex](https://example.com/test.png?size=large&format=png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("complex", "https://example.com/test.png?size=large&format=png")], matches)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "This a test with an ![first](https://i.imgur.com/xyz) and ![second](https://i.imgur.com/zyx)"
        )
        self.assertListEqual([("first", "https://i.imgur.com/xyz"), ("second", "https://i.imgur.com/zyx")], matches)

    def test_no_images(self):
        text = "Plain text"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_no_alt_text(self):
        text = "This is an ![](https://i.imgur.com/xyz)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://i.imgur.com/xyz")], matches)

    def test_regular_links(self):
        text = "This is a [link](https://i.imgur.com/xyz) but no images."
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_complex_urls(self):
        text = '![complex](https://example.com/index.php?query="how-does-it-work"&filter=none)'
        matches = extract_markdown_images(text)
        self.assertListEqual([("complex", 'https://example.com/index.php?query="how-does-it-work"&filter=none')], matches)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        old_nodes = [TextNode("This is an ![image](https://example.com) and not much else", TextType.TEXT)]
        expected_result = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com"),
            TextNode(" and not much else", TextType.TEXT)
        ]
        self.assertListEqual(split_nodes_image(old_nodes), expected_result)

    def test_multiple_images(self):
        old_nodes = [TextNode("This is the ![first](https://example.com/1.jpg) and the ![second](https://example.com/2.jpg) image", TextType.TEXT)]
        expected_results = [
            TextNode("This is the ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "https://example.com/1.jpg"),
            TextNode(" and the ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "https://example.com/2.jpg"),
            TextNode(" image", TextType.TEXT)
        ]
        self.assertListEqual(split_nodes_image(old_nodes), expected_results)

    def test_multiple_nodes_with_images(self):
        old_nodes = [
            TextNode("This is the ![first](https://example.com/1.jpg) and the ![second](https://example.com/2.jpg) image", TextType.TEXT),
            TextNode("This is an ![image](https://example.com/test.jpg)", TextType.TEXT)
            ]
        expected_results = [
            TextNode("This is the ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "https://example.com/1.jpg"),
            TextNode(" and the ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "https://example.com/2.jpg"),
            TextNode(" image", TextType.TEXT),
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/test.jpg")
        ]
        self.assertListEqual(split_nodes_image(old_nodes), expected_results)

    def test_multiple_nodes_mixed_content(self):
        old_nodes = [
            TextNode("This is the ![first](https://example.com/1.jpg) and the ![second](https://example.com/2.jpg) image", TextType.TEXT),
            TextNode("This is an ![image](https://example.com/test.jpg)", TextType.TEXT),
            TextNode("This is a [link](https://example.com)", TextType.TEXT),
            TextNode("Click Me!", TextType.LINK, "https://example.com/test.sh"),
            TextNode("Dog pics", TextType.IMAGE, "https://example.com/dog.jpg")
            ]
        expected_results = [
            TextNode("This is the ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "https://example.com/1.jpg"),
            TextNode(" and the ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "https://example.com/2.jpg"),
            TextNode(" image", TextType.TEXT),
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/test.jpg"),
            TextNode("This is a [link](https://example.com)", TextType.TEXT),
            TextNode("Click Me!", TextType.LINK, "https://example.com/test.sh"),
            TextNode("Dog pics", TextType.IMAGE, "https://example.com/dog.jpg")
        ]
        self.assertListEqual(split_nodes_image(old_nodes), expected_results)

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

if __name__ == "__main__":
    unittest.main()