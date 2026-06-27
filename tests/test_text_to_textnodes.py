import unittest

from src.textnode import TextNode, TextType
from src.converters import split_nodes_image, split_nodes_link, text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_one(self):
        to_check = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(to_check)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], result
        )


    def test_plain_text_only(self):
        text = "Just plain text with no markdown."
        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("Just plain text with no markdown.", TextType.PLAIN),
            ],
            result,
        )


    def test_only_bold(self):
        text = "**hello**"
        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("hello", TextType.BOLD),
            ],
            result,
        )


    def test_multiple_bold(self):
        text = "**one** and **two**"
        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("two", TextType.BOLD),
            ],
            result,
        )


    def test_multiple_italics(self):
        text = "_one_ _two_ _three_"
        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("one", TextType.ITALIC),
                TextNode(" ", TextType.PLAIN),
                TextNode("two", TextType.ITALIC),
                TextNode(" ", TextType.PLAIN),
                TextNode("three", TextType.ITALIC),
            ],
            result,
        )


    def test_code_at_beginning(self):
        text = "`print()` is Python"
        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("print()", TextType.CODE),
                TextNode(" is Python", TextType.PLAIN),
            ],
            result,
        )


    def test_code_at_end(self):
        text = "Use `git status`"
        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("Use ", TextType.PLAIN),
                TextNode("git status", TextType.CODE),
            ],
            result,
        )


    def test_image_only(self):
        text = "![cat](https://example.com/cat.png)"
        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode(
                    "cat",
                    TextType.IMAGE,
                    "https://example.com/cat.png",
                ),
            ],
            result,
        )


    def test_link_only(self):
        text = "[Boot.dev](https://boot.dev)"
        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://boot.dev",
                ),
            ],
            result,
        )


    def test_multiple_links_and_images(self):
        text = (
            "[one](https://one.com) "
            "![img](https://img.com/a.png) "
            "[two](https://two.com)"
        )

        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "https://one.com"),
                TextNode(" ", TextType.PLAIN),
                TextNode("img", TextType.IMAGE, "https://img.com/a.png"),
                TextNode(" ", TextType.PLAIN),
                TextNode("two", TextType.LINK, "https://two.com"),
            ],
            result,
        )


    def test_all_styles_together(self):
        text = "**bold** _italic_ `code`"

        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
            ],
            result,
        )


    def test_unclosed_bold(self):
        with self.assertRaises(Exception):
            text_to_textnodes("This is **broken")


    def test_unclosed_italic(self):
        with self.assertRaises(Exception):
            text_to_textnodes("_broken")


    def test_unclosed_code(self):
        with self.assertRaises(Exception):
            text_to_textnodes("`print('hello')")


    def test_everything_interleaved(self):
        text = (
            "A **bold** B _italic_ C "
            "`code` D [link](https://a.com) "
            "E ![img](https://b.com/img.png) F"
        )

        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("A ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" B ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" C ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" D ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://a.com"),
                TextNode(" E ", TextType.PLAIN),
                TextNode("img", TextType.IMAGE, "https://b.com/img.png"),
                TextNode(" F", TextType.PLAIN),
            ],
            result,
        )