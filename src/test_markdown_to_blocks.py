import unittest

from helper_functions import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_extra_blank_lines(self):
        md = """
    This is **bolded** to alert you that there will be three newlines below.



    The test is over now.
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,[
                "This is **bolded** to alert you that there will be three newlines below.",
                "The test is over now."
            ]
            )
        
    def test_whitespace_irregularity(self):
        md = """
        This is a line\n
           This is a line      

        
        This is a line
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,[
               "This is a line",
               "This is a line",
               "This is a line" 
            ]
        )

    def test_empty_markdown(self):
        md = """
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_block(self):
        md = """
    This is a single block.
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block."])
    
    def test_complex_markdown(self):
        md = """
    **This is a test article that is written about testing.***
    It will contain complex arrangements of _markdown_ emphasis markers, ![images](https://example.com/images) and [links](https://example.com).

    
    For example, this is the **main paragraph** block, which is where the code will be described that is contained below. This _code_ is
    a basic function to print "Hello, World" to the stdout console/terminal. A terminal used to look like ![this](https://example.com/terminal.jpg),
    but now it is just an interactive GUI on your computer. 

    
    `sudo rm dir -r` will print "Hello, World" to terminal when ran from terminal.
    """
        blocks = markdown_to_blocks(md)
        expected_result = [
        "**This is a test article that is written about testing.***\n"
        "It will contain complex arrangements of _markdown_ emphasis markers, "
        "![images](https://example.com/images) and [links](https://example.com).",
    
        "For example, this is the **main paragraph** block, which is where the code will be described that is contained below. "
        "This _code_ is\n"
        'a basic function to print "Hello, World" to the stdout console/terminal. '
        "A terminal used to look like ![this](https://example.com/terminal.jpg),\n"
        "but now it is just an interactive GUI on your computer.",
    
        "`sudo rm dir -r` will print \"Hello, World\" to terminal when ran from terminal."
        ]   
        self.assertEqual(blocks, expected_result)