import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_constructor_defaults(self):
        node = HTMLNode()

        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_exception(self):
        html_node1 = HTMLNode("h1", "My first Test")
        with self.assertRaises(NotImplementedError):
            html_node1.to_html()

    def test_props_to_html_result(self):
        expected = ' href="https://www.google.com" target="_blank"'
        prop_dict = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        html_node1 = HTMLNode("a", "Click Here", None, prop_dict)
        self.assertEqual(html_node1.props_to_html(), expected)


if __name__ == "__main__":
    unittest.main()