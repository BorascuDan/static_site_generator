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
    
_DELIMITORS = {'**':TextType.BOLD, '_':TextType.ITALIC, '`':TextType.CODE}

def split_nodes_delimitor(old_nodes):
    new_nodes = []
    for i in range(len(old_nodes)):
        node = old_nodes[i]
        if node.text_type == TextType.TEXT:
            new_nodes.extend(split_node(node))
        else:
            new_nodes.append(node)

    return new_nodes     

def split_node(old_node):
    oldText = old_node.text
    stack = []

    for i in range(len(oldText)):
        char = oldText[i]
        if char in _DELIMITORS:
            stack.append([char, i])

    size = len(stack)
    if size % 2 != 0:
        raise Exception("This is not propper Markdown syntax")
    
    new_nodes = []
    new_nodes.append(TextNode(text=oldText[0:stack[0][1]]))
    for i in range(size - 1):
        if stack[i][0] != stack[size - i - 1][0]:
            raise Exception("This is not propper Markdown syntax")
        new_nodes.append(TextNode(text=oldText[stack[i][1] + 1:stack[i + 1][1]], text_type=_DELIMITORS[stack[i][0]]))

    lastTransform = stack.pop()
    if lastTransform[1] < len(oldText):
        new_nodes.append(TextNode(text=oldText[lastTransform[1] + 1:]))
    
    return new_nodes