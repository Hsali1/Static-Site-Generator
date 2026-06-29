from src.converters import markdown_to_html_node
from src.htmlnode import ParentNode, LeafNode
import os


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No h1 header found.")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        markdown_file_contents = file.read()
    
    with open(template_path, 'r') as file:
        template_file_contents = file.read()

    get_parent_div_node: ParentNode = markdown_to_html_node(markdown_file_contents)
    get_html_string_of_parent_div_node: str = get_parent_div_node.to_html()

    page_title: str = extract_title(markdown_file_contents)

    template_file_contents.replace("\{\{ Title \}\}", page_title)
    template_file_contents.replace("\{\{ Content \}\}", get_html_string_of_parent_div_node)

    dest_path_with_file = os.path.normpath(os.path.join(dest_path, "index.html"))

    with open(dest_path_with_file, 'w') as file:
        file.write(template_file_contents)