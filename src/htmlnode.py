class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def props_to_html(self):
        
        if not self.props:
            return ""

        atribute_values = []

        for atribut, value in self.props.items():
            curentAtribute = f'{atribut}="{value}"'
            atribute_values.append(curentAtribute)

        return " ".join(atribute_values)

    def __repr__(self):
       return f'tag={self.tag}, value={self.value}, children={self.children}, props={self.props}'