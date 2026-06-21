import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_with_props(self):
        prop_dict = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        expected = '<a href="https://www.google.com" target="_blank">Click me!</a>'
        node2 = LeafNode("a", "Click me!", prop_dict)
        self.assertEqual(node2.to_html(), expected)
