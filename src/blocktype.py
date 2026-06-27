from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("#"):
        hashes = len(block) - len(block.lstrip("#"))

        if 1 <= hashes <= 6 and block[hashes:].startswith(" "):
            return BlockType.HEADING
        
        return BlockType.PARAGRAPH
        
    if block.startswith("```"):
        if block.endswith("```"):
            return BlockType.CODE
        return BlockType.PARAGRAPH
    
    if block.startswith(">"):
        for line in block.split("\n"):
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if block.startswith("- "):
        for line in block.split("\n"):
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    lines = block.split("\n")
    expected = 1

    for line in lines:
        if not line.startswith(f"{expected}. "):
            return BlockType.PARAGRAPH
        expected += 1

    return BlockType.ORDERED_LIST