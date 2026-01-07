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

        if len(splits) == 0:
            res.append(node)
            continue

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


def condition_type_a(i, old_text, str_url_tuplet, current_link):
    return (
        i < len(old_text) - 2
        and old_text[i] == "!"
        and old_text[i + 1] == "["
        and old_text[i + 2] == str_url_tuplet[current_link][0][0]
    )


def condition_type_b(i, old_text, str_url_tuplet, current_link):
    return (
        i < len(old_text) - 1
        and old_text[i] == "["
        and old_text[i + 1] == str_url_tuplet[current_link][0][0]
    )


_CONDITION_MAP = {
    "image": condition_type_a,
    "url": condition_type_b,
}

_EXTRACT_MARKDOW = {
    "image": extract_markdown_images,
    "url": extract_markdown_links,
}

_TEXT_TYPE = {
    "image": TextType.IMAGE,
    "url": TextType.LINK,
}


def split_nodes_url(old_nodes, url_type):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue

        old_text = node.text
        str_url_tuplet = _EXTRACT_MARKDOW[url_type](old_text)
        if not len(str_url_tuplet):
            res.append(node)
            continue

        new_nodes = []
        curent_link = 0
        startIndex = 0
        i = 0
        while i < len(old_text):
            if _CONDITION_MAP[url_type](i, old_text, str_url_tuplet, curent_link):
                if i != 0:
                    new_nodes.append(
                        TextNode(old_text[startIndex:i], text_type=TextType.TEXT)
                    )
                new_nodes.append(
                    TextNode(
                        str_url_tuplet[curent_link][0],
                        text_type=_TEXT_TYPE[url_type],
                        url=str_url_tuplet[curent_link][1],
                    )
                )
                i = (
                    i
                    + len(str_url_tuplet[curent_link][0])
                    + len(str_url_tuplet[curent_link][1])
                )

                i += 5 if url_type == "image" else 4
                curent_link += 1
                startIndex = i
            else:
                i += 1

        if startIndex != len(old_text):
            new_nodes.append(TextNode(old_text[startIndex:], text_type=TextType.TEXT))

        res.extend(new_nodes)

    return res


def split_nodes_image(old_nodes):
    return split_nodes_url(old_nodes, "image")


def split_nodes_link(old_nodes):
    return split_nodes_url(old_nodes, "url")


_NODE_TYPE_TEXT = {
    "**": TextType.BOLD,
    "_": TextType.ITALIC,
    "`": TextType.CODE,
}


def text_to_textnode(text):
    old_nodes = [TextNode(text, TextType.TEXT)]
    for key, value in _NODE_TYPE_TEXT.items():
        old_nodes = split_nodes_delimiter(old_nodes, key, value)

    old_nodes = split_nodes_image(old_nodes)
    old_nodes = split_nodes_link(old_nodes)
    return old_nodes
