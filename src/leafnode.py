from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if not self.tag:
            return self.value

        if not self.value and self.tag != "img":
            raise ValueError

        props = super().props_to_html()

        return (
            f"<{self.tag} {props}>{self.value}</{self.tag}>"
            if props
            else f"<{self.tag}>{self.value}</{self.tag}>"
        )
