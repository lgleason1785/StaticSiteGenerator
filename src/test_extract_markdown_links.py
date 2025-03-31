import unittest

from helper_functions import extract_markdown_links

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