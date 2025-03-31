import unittest

from enums import BlockType
from helper_functions import block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_block(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        failed_block = "####### This is invalid"
        self.assertNotEqual(block_to_block_type(failed_block), BlockType.HEADING)
    
    def test_code_block(self):
        block = "```This is a\ncode block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        failed_block = "``` This is invalid"
        self.assertNotEqual(block_to_block_type(failed_block), BlockType.CODE)
    
    def test_quote_block(self):
        block = ">This is a quote\n>and continuation"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        failed_block = ">This is\ninvalid"
        self.assertNotEqual(block_to_block_type(failed_block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- This is a\n- unordered list"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        failed_block = "- This is\n-invalid"
        self.assertNotEqual(block_to_block_type(failed_block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. This\n2. is\n3. an ordered list"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        failed_block = "1. This\n3. is\n4. invalid"
        self.assertNotEqual(block_to_block_type(failed_block), BlockType.ORDERED_LIST)