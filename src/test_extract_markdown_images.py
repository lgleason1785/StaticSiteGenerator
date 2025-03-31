import unittest

from helper_functions import extract_markdown_images

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

    