from markdown_to_blocks import markdown_to_blocks
from blocktype import block_to_block_type, BlockType
from htmlnode import ParentNode, LeafNode 
from inline_markdown import text_to_textnodes
from textnode import TextType

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    print(f"DEBUG: Nombre de blocs trouvés: {len(blocks)}") 
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING:
            level = len(block) - len(block.lstrip('#'))
            text = block[level:].strip()
            children.append(ParentNode(f"h{level}", text_to_children(text)))

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                content = line[2:].strip()
                li_nodes.append(ParentNode("li", text_to_children(content)))
            children.append(ParentNode("ul", li_nodes))

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                content = line[line.find(" ") + 1:].strip()
                li_nodes.append(ParentNode("li", text_to_children(content)))
            children.append(ParentNode("ol", li_nodes))

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            content = " ".join([line.lstrip(">").strip() for line in lines])
            children.append(ParentNode("blockquote", text_to_children(content)))

        elif block_type == BlockType.CODE:
            content = block.strip("`").strip()
            children.append(ParentNode("pre", [LeafNode("code", content)]))

        else: # PARAGRAPH
            children.append(ParentNode("p", text_to_children(block)))
            
    return ParentNode("div", children)