import os
import sys

from src.textnode import TextNode, TextType
from src.converters import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_html_node,
)

from src.copy_static_to_public import copy_static_to_public
from src.page_functions import extract_title, generate_page, generate_pages_recursive

def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = '/'

    source_directory = "static"
    destination_directory = "docs"
    copy_static_to_public(source_directory, destination_directory)

    markdown_path = "content/"
    template_path = "./template.html"
    destination_path = "docs/"


    # generate_page(markdown_path, template_path, destination_path)
    generate_pages_recursive(markdown_path,
                             template_path,
                             destination_path,
                             basepath)



main()