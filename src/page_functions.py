from src.converters import markdown_to_html_node
from src.htmlnode import ParentNode
import os


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No h1 header found.")


def generate_page(from_path: str,
                  template_path: str,
                  dest_path: str,
                  base_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        markdown_file_contents = file.read()
    
    with open(template_path, 'r') as file:
        template_file_contents = file.read()

    get_parent_div_node: ParentNode = markdown_to_html_node(markdown_file_contents)
    get_html_string_of_parent_div_node: str = get_parent_div_node.to_html()

    page_title: str = extract_title(markdown_file_contents)

    # template_file_contents.replace("\{\{ Title \}\}", page_title)
    template_file_contents = template_file_contents.replace("{{ Title }}",
                                                            page_title)
    template_file_contents = template_file_contents.replace("{{ Content }}",
                                                            get_html_string_of_parent_div_node)

    template_file_contents = template_file_contents.replace("href=\"/",
                                                            f"href=\"{base_path}")
    template_file_contents = template_file_contents.replace("src=\"/",
                                                            f"src=\"{base_path}")

    destination_dir = os.path.dirname(dest_path)

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    with open(dest_path, 'w') as file:
        file.write(template_file_contents)


def generate_pages_recursive(dir_path_content: str,
                             template_path: str,
                             dest_dir_path: str,
                             base_path: str):

    current_directory = os.path.abspath(dir_path_content)
    # print(f"cwd = {current_working_directory}")

    dest_dir_abs_path = os.path.abspath(dest_dir_path)
    # print(f"dest_dir_abs_path = {dest_dir_abs_path}")
    
    list_of_content_items = os.listdir(current_directory)
    # print(f"  {list_of_content_items}")
    
    for content_item in list_of_content_items:

        # print(f"   currently looking at {content_item}")

        content_item_path = os.path.normpath(os.path.join(current_directory,
                                                          content_item))

        if not os.path.isdir(content_item_path):
            if os.path.splitext(content_item_path)[1].lower() != ".md": 
                continue
            # print(f"----recursion-end--{content_item} is a file")
            dest_dir_abs_path_with_file = os.path.normpath(os.path.join(dest_dir_abs_path,
                                                                        "index.html"))
            # print(f"from_path = {content_item_path}")
            # print(f"dest_path = {dest_dir_abs_path_with_file}")
            # print("---")
            generate_page(content_item_path,
                          template_path,
                          dest_dir_abs_path_with_file,
                          base_path)
        else:
            # print(f"++++{content_item} is a folder")
            dest_dir_content_item_path = os.path.normpath(os.path.join(dest_dir_abs_path,
                                                                       content_item))
            # print(f"Recursing... going into {content_item_path}")
            generate_pages_recursive(content_item_path,
                                     template_path,
                                     dest_dir_content_item_path,
                                     base_path)