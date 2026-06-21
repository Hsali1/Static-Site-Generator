"""
Defines the HTML node hierarchy used to generate HTML output.

HTMLNode is the abstract base class for all HTML nodes and stores:
- an HTML tag
- optional text content
- optional child nodes
- optional HTML attributes (props)

LeafNode represents a node with text content and no children
(e.g. text, links, images, code).

ParentNode represents a node that contains one or more child nodes
(e.g. paragraphs, headings, divs).

Pipeline:

Markdown text
    ↓
TextNode objects
    ↓
HTMLNode tree (this file)
    ↓
HTML string output
"""

class HTMLNode():
    def __init__(self,
                 tag: str = None,
                 value: str = None,
                 children: list["HTMLNode"] = None,
                 props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This is meant to be overloaded.")
    
    def props_to_html(self):
        result = ''
        if self.props is None or not len(self.props):
            return result
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
    
    def __repr__(self):
        return {
            "tag": self.tag,
            "value": self.value,
            "children": self.children,
            "props": self.props
        }
    

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("self.value cannot be None")
        if self.tag is None:
            return self.value
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return {
            "tag": self.tag,
            "value": self.value,
            "props": self.props
        }
    

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("self.tag cannot be None")
        if not self.children:
            raise ValueError("self.children cannot be None/empty")
        props = self.props_to_html()
        result = f"<{self.tag}{props}>"

        for child in self.children:
            result += child.to_html()

        result += f"</{self.tag}>"

        return result
        
        
