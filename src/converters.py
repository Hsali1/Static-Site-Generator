import re

from pkg_resources import split_sections

from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import TextNode, TextType

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            prop_dict = {
                "href": text_node.url
            }
            return LeafNode('a', text_node.text, prop_dict)
        case TextType.IMAGE:
            prop_dict = {
                "src": text_node.url,
                "alt": text_node.text
            }
            return LeafNode("img", "", prop_dict)
        case _:
            raise Exception("text_node.text_type MUST be of type TextType")
        

def split_nodes_delimiter(
        old_nodes: list[TextNode],
        delimeter: str,
        text_type: TextType) -> list[TextNode]:
    
    result = []

    for text_node in old_nodes:
        if text_node.text_type is not TextType.PLAIN:
            result.append(text_node)
            continue
        new_nodes = text_node.text.split(delimeter)
        if len(new_nodes) % 2 == 0:
            raise Exception("Invalid input. There needs to be a closing delimater")
        for i, part in enumerate(new_nodes):
            if part == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(part, TextType.PLAIN))
            else:
                result.append(TextNode(part, text_type))

    return result
    

def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []

    for text_node in old_nodes:
        # example: This is text with a image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)
        if text_node.text_type is not TextType.PLAIN:
            result.append(text_node)
            continue
        extract_alt_and_link = extract_markdown_images(text_node.text)
        # example: [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        if len(extract_alt_and_link) == 0:
            result.append(text_node)
            continue
        text_node_text = text_node.text
        # print(f"Before - {text_node_text}")
        for image_alt, image_link in extract_alt_and_link:
            sections = text_node_text.split(f"![{image_alt}]({image_link})", 1)
            # print(f"    -sections[0] = {sections[0]}")
            # print(f"    -sections[1] = {sections[1]}")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.PLAIN))
            result.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text_node_text = sections[1]
            # print(f"After iter - {text_node_text}")

        if text_node_text != "":
            result.append(TextNode(text_node_text, TextType.PLAIN))

        # print(f"After loop, result:")
        print(result)

    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    pass