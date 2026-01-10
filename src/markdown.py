from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdow):
    blocks = markdow.split("\n\n")

    formated_blocks = []
    for block in blocks:
        striped = block.strip()
        if len(striped) == 0:
            continue

        formated_blocks.append(striped)

    return formated_blocks


def block_to_block_type(block):
    if re.match(r"^#{1,6}\s+", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if re.match(r"^(?:> .*)(?:\n> .*)*$", block):
        return BlockType.QUOTE
    if re.match(r"^(?:- .*)(?:\n- .*)*$", block):
        return BlockType.UNORDERED_LIST

    lines = block.splitlines()
    for i, line in enumerate(lines, start=1):
        prefix = f"{i}. "
        if not line.startswith(prefix):
            return BlockType.PARAGRAPH

    return BlockType.ORDERED_LIST
