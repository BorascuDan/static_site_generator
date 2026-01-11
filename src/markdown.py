from enum import Enum
import re
from leafnode import LeafNode
from src.utilFunctions import text_node_to_html_node, text_to_textnode
from src.textnode import TextNode, TextType
from src.parentnode import ParentNode


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


_HTML_TAG = {
    BlockType.CODE: lambda _: "pre",
    BlockType.QUOTE: lambda _: "blockquote",
    BlockType.ORDERED_LIST: lambda _: "ol",
    BlockType.UNORDERED_LIST: lambda _: "ul",
    BlockType.PARAGRAPH: lambda _: "p",
    BlockType.HEADING: lambda s: f"h{len(s) - len(s.lstrip('#'))}",
}

_TEXT_TYPE = {
    TextType.ITALIC: "i",
    TextType.CODE: "code",
    TextType.BOLD: "b",
    TextType.TEXT: "",
    TextType.IMAGE: "img",
    TextType.LINK: "a",
}


def block_to_html(block):
    block_type = block_to_block_type(block)
    block_text = None
    if block_type == BlockType.ORDERED_LIST or block_type == BlockType.UNORDERED_LIST:
        normalized = block.split("\n")
        block_text = [s[2:].strip() for s in normalized]
        text_nodes = list(map(text_to_textnode, block_text))
        html_items = [
            [
                LeafNode(tag=_TEXT_TYPE[node.text_type], value=node.text)
                for node in list_item
            ]
            for list_item in text_nodes
        ]

        html_nodes = list(map(lambda s: ParentNode(tag="li", children=s), html_items))
    elif block_type == BlockType.CODE:
        block_text = [TextNode(text=block[4 : len(block) - 3], text_type=TextType.CODE)]
        html_nodes = list(map(text_node_to_html_node, block_text))
    else:
        normalized = block.replace("> ", "").replace("\n", " ").replace("#", "").strip()
        block_text = text_to_textnode(normalized)
        html_nodes = list(map(text_node_to_html_node, block_text))

    return ParentNode(tag=_HTML_TAG[block_type](block), children=html_nodes)


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    html = list(map(block_to_html, markdown_blocks))
    return ParentNode(tag="div", children=html)
