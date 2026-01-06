from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text="", text_type=TextType.TEXT, url=None):
        # The text content of the node
        self.text = text

        # The type of text this node contains (member of TextType)
        self.text_type = text_type

        # The URL of the link or image, if applicable
        self.url = url

    def __eq__(self, node):
        if (
            self.text == node.text
            and self.text_type == node.text_type
            and self.url == node.url
        ):
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode(text={self.text!r}, type={self.text_type.value}, url={self.url!r})"
