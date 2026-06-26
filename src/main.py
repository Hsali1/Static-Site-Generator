from src.textnode import TextNode, TextType
from src.converters import split_nodes_delimiter, split_nodes_image, split_nodes_link

def main():
    node = TextNode(
        "This is text with a image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_image([node])

main()