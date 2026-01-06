import re
from src.textnode import TextType, TextNode
from src.leafnode import LeafNode


def _text(node):
    return LeafNode(value=node.text)


def _bold(node):
    return LeafNode(tag="b", value=node.text)


def _italic(node):
    return LeafNode(tag="i", value=node.text)


def _code(node):
    return LeafNode(tag="code", value=node.text)


def _link(node):
    return LeafNode(tag="a", value=node.text, props={"href": node.url})


def _image(node):
    return LeafNode(tag="img", value="", props={"src": node.url, "alt": node.text})


_DISPATCH = {
    TextType.TEXT: _text,
    TextType.BOLD: _bold,
    TextType.ITALIC: _italic,
    TextType.CODE: _code,
    TextType.LINK: _link,
    TextType.IMAGE: _image,
}


def text_node_to_html_node(node):
    try:
        return _DISPATCH[node.text_type](node)
    except KeyError:
        raise ValueError(f"Unhandled TextType: {node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue

        old_text = None
        if delimiter == "**":
            old_text = node.text.replace("**", "*")
            delimiter = "*"
        else:
            old_text = node.text

        splits = []
        i = 0
        while i < len(old_text):
            if delimiter == "**":
                if (
                    i + 1 < len(old_text)
                    and old_text[i] == "*"
                    and old_text[i + 1] == "*"
                ):
                    splits.append(i)
                    i += 2
                    continue
            else:
                if old_text[i] == delimiter:
                    splits.append(i)
            i += 1

        if len(splits) % 2 != 0:
            raise Exception("Not propper markdown")

        new_nodes = []
        if splits[0] != 0:
            new_nodes.append(TextNode(old_text[0 : splits[0]], text_type=TextType.TEXT))

        for i in range(len(splits)):
            curent_text_type = text_type if i % 2 == 0 else TextType.TEXT
            delim_len = 2 if delimiter == "**" else 1
            left = splits[i] + delim_len
            right = splits[i + 1] if i != len(splits) - 1 else len(old_text)
            if left == right:
                break
            new_nodes.append(TextNode(old_text[left:right], text_type=curent_text_type))

        res.extend(new_nodes)

    return res


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
