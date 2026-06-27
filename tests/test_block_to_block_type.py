import unittest

from src.blocktype import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_heading_h1(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)


    def test_heading_h6(self):
        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)


    def test_invalid_heading_too_many_hashes(self):
        block = "####### Not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)


    def test_quote_single_line(self):
        block = ">Hello"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


    def test_quote_multiple_lines(self):
        block = ">Hello\n>World"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


    def test_invalid_quote(self):
        block = ">Hello\nWorld"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_unordered_list(self):
        block = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)


    def test_invalid_unordered_list(self):
        block = "- one\ntwo\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)


    def test_invalid_ordered_list_starts_at_two(self):
        block = "2. one\n3. two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_invalid_ordered_list_skips_number(self):
        block = "1. one\n3. two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_invalid_ordered_list_missing_space(self):
        block = "1.one\n2.two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)