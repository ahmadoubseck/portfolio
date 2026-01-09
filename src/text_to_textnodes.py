from textnode import TextNode, TextType
from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


def text_to_textnodes(text):
    # 1. point de départ : tout le texte est TEXT
    nodes = [TextNode(text, TextType.TEXT)]

    # 2. images
    nodes = split_nodes_image(nodes)

    # 3. liens
    nodes = split_nodes_link(nodes)

    # 4. gras
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # 5. italique (_ ou *)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    # 6. code
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
