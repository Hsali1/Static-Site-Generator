import unittest

from src.textnode import TextNode, TextType
from src.converters import split_nodes_delimiter

class TestConverterSplitNodes(unittest.TestCase):
    def test_single_node_with_one_delimeter(self):

        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]

        self.assertEqual(len(new_nodes), len(expected))

        for i in enumerate(expected):
            self.assertEqual(expected[0], new_nodes[0])


    def test_single_node_with_many_delimeter(self):
        node = TextNode("_This_ is **text** with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("_This_ is **text** with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]

        self.assertEqual(len(new_nodes), len(expected))

        for i in enumerate(expected):
            self.assertEqual(expected[0], new_nodes[0])

    
    def test_multiple_nodes_with_single_delimeter(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        node2 = TextNode("This is 2nd text with a `code block` word", TextType.PLAIN)
        node3 = TextNode("This is 3rd text with a `code block` word", TextType.PLAIN)

        new_nodes = split_nodes_delimiter([node, node2, node3], "`", TextType.PLAIN)

        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
            TextNode("This is 2nd text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
            TextNode("This is 3rd text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]

        self.assertEqual(len(new_nodes), len(expected))

        for i in enumerate(expected):
            self.assertEqual(expected[0], new_nodes[0])