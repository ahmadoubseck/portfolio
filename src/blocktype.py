from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    # 1. Code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # 2. Heading
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # 3. Quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # 4. Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # 5. Ordered list
    ordered = True
    for i, line in enumerate(lines):
        if not line.startswith(f"{i+1}. "):
            ordered = False
            break
    if ordered:
        return BlockType.ORDERED_LIST

    # 6. Paragraph (par défaut)
    return BlockType.PARAGRAPH
