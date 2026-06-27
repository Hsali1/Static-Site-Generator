import re
from typing import Text

from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import TextNode, TextType
from src.blocktype import block_to_block_type, BlockType


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
        # print(result)

    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []

    for text_node in old_nodes:
        if text_node.text_type is not TextType.PLAIN:
            result.append(text_node)
            continue
        extract_text_and_url = extract_markdown_links(text_node.text)
        if len(extract_text_and_url) == 0:
            result.append(text_node)
            continue
        text_node_text = text_node.text
        for link_text, link_url in extract_text_and_url:
            sections = text_node_text.split(f"[{link_text}]({link_url})", 1)

            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.PLAIN))
            result.append(TextNode(link_text, TextType.LINK, link_url))
            text_node_text = sections[1]

        if text_node_text != "":
            result.append(TextNode(text_node_text, TextType.PLAIN))

    return result


def text_to_textnodes(text) -> list[TextNode]:
    bold_list = split_nodes_delimiter([TextNode(text, TextType.PLAIN)], "**", TextType.BOLD)
    bold_italic_list = split_nodes_delimiter(bold_list, "_", TextType.ITALIC)
    bold_italic_code_list = split_nodes_delimiter(bold_italic_list, "`", TextType.CODE)
    bold_italic_code_image_list = split_nodes_image(bold_italic_code_list)
    bold_italic_code_image_link_list = split_nodes_link(bold_italic_code_image_list)


    return bold_italic_code_image_link_list


def markdown_to_blocks(markdown: str) -> list[str]:
    result = []

    no_white_space_markdown = markdown.strip()
    split_markdown = no_white_space_markdown.split("\n\n")

    for block in split_markdown:
        block.strip()

        if len(block) != 0:
            result.append(block)

    return result


def text_to_children(block: str) -> list[HTMLNode]:
    text_nodes: list[TextNode] = text_to_textnodes(block)
    html_nodes: list[HTMLNode] = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def markdown_to_html_node(markdown: str):
    markdown_block_list: list[str] = markdown_to_blocks(markdown)
    parent_node_list = []
    for markdown_block in markdown_block_list:
        markdown_block_type: BlockType = block_to_block_type(markdown_block)
        # markdown_block_type = <BlockType.PARAGRAPH: 'paragraph'>

        match markdown_block_type:
            case BlockType.PARAGRAPH:
                new_lines_removed_markdown = markdown_block.replace('\n', ' ')
                inline_html_nodes_for_paragraph = text_to_children(new_lines_removed_markdown)
                paragraph_parent_node = ParentNode('p', inline_html_nodes_for_paragraph)
                parent_node_list.append(paragraph_parent_node)
            case BlockType.UNORDERED_LIST:
                individual_item_parent_nodes = []
                individual_item_in_list = markdown_block.split('\n')
                for individual_item in individual_item_in_list:
                    individual_item = individual_item[2:]
                    individual_item_children_html_nodes = text_to_children(individual_item)
                    individual_item_parent_node = ParentNode('li', individual_item_children_html_nodes)
                    individual_item_parent_nodes.append(individual_item_parent_node)
                complete_unordered_list_block = ParentNode('ul', individual_item_parent_nodes)
                parent_node_list.append(complete_unordered_list_block)
            case BlockType.ORDERED_LIST:
                individual_item_parent_nodes = []
                individual_item_in_list = markdown_block.split('\n')
                for individual_item in individual_item_in_list:
                    individual_item = individual_item.split(". ", 1)
                    individual_item = individual_item[1]
                    individual_item_children_html_nodes = text_to_children(individual_item)
                    individual_item_parent_node = ParentNode('li', individual_item_children_html_nodes)
                    individual_item_parent_nodes.append(individual_item_parent_node)
                complete_ordered_list_block = ParentNode('ol', individual_item_parent_nodes)
                parent_node_list.append(complete_ordered_list_block)
            case BlockType.CODE:
                # stripped_code_block = markdown_block.strip("```")
                stripped_code_block = markdown_block[4:-3]  # removes "```\n" at start and "```" at end
                code_text_node = TextNode(stripped_code_block, TextType.PLAIN)
                code_html_node = text_node_to_html_node(code_text_node)

                parent_pre_node = ParentNode("pre", [ParentNode("code", [code_html_node])])
                parent_node_list.append(parent_pre_node)
            case BlockType.QUOTE:
                individual_quotes = markdown_block.split("\n")
                processed_quote_list = []
                for quote in individual_quotes:
                    quote = quote[1:]
                    quote = quote.strip()
                    processed_quote_list.append(quote)
                processed_quotes_back_in_str = " ".join(processed_quote_list)
                inline_html_nodes_for_quote = text_to_children(processed_quotes_back_in_str)
                parent_quote_html_node_for_quote = ParentNode('blockquote', inline_html_nodes_for_quote)
                parent_node_list.append(parent_quote_html_node_for_quote)
            case BlockType.HEADING:
                stripped_markdown_block = markdown_block.lstrip('#')
                heading_levels = len(markdown_block) - len(stripped_markdown_block)
                stripped_markdown_block = stripped_markdown_block.lstrip(' ')
                heading_child_inline_items = text_to_children(stripped_markdown_block)
                parent_heading_html_node = ParentNode(f"h{heading_levels}", heading_child_inline_items)
                parent_node_list.append(parent_heading_html_node)
            case _:
                raise Exception("unknown block type")

    return ParentNode('div', parent_node_list)