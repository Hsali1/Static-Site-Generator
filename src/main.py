import os

from src.textnode import TextNode, TextType
from src.converters import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_html_node,
)

from src.copy_static_to_public import copy_static_to_public
from src.page_functions import extract_title, generate_page

def main():
    source_directory = "static"
    destination_directory = "public"
    copy_static_to_public(source_directory, destination_directory)


    # generate_page()


main()