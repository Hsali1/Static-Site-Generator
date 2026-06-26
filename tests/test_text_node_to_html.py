import unittest
from src.textnode import TextNode, TextType
from src.converters import text_node_to_html_node
from src.htmlnode import LeafNode

class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_return_typ(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)

    def test_text_print(self):
        text_inp = "This is a text node"
        text_type_inp = TextType.PLAIN
        node = TextNode(text_inp, text_type_inp)
        html_node = text_node_to_html_node(node)
        expected = f"LeafNode(tag={None}, value={text_inp!r}, props={None})"
        self.assertEqual(expected, html_node.__repr__())

    def test_link_html(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(html_node.to_html(), expected)

