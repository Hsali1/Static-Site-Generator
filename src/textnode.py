"""
Defines the intermediate representation used while converting Markdown to HTML.

TextType enumerates the supported inline Markdown elements
(plain text, bold, italic, code, links, and images).

TextNode represents a single piece of inline content and stores:
- the text content
- the type of content
- an optional URL (for links and images)

These objects are produced during Markdown parsing and later
converted into HTML nodes.
"""

from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type: TextType, url: str=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode") -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"