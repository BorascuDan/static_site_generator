from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        if tag is None or children is None:
            raise Exception("tag and children are required")

        self.html = ""
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError('tag is mandatory')
        
        if self.children is None:
            raise ValueError("children is mandatory")
        
        props = super().props_to_html()

        rezult = ""
        for child in self.children:
            rezult += child.to_html()

        return (
                f'<{self.tag} {props}>{rezult}</{self.tag}>'
                if props
                else f'<{self.tag}>{rezult}</{self.tag}>'
            )
