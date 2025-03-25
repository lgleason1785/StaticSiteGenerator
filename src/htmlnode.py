class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props: # Covers both `None` and empty `{}` 
            return ""
        
        formatted_props = map(
            lambda item: f'{item[0]}="{item[1]}"', self.props.items()
        )
        return " " + " ".join(formatted_props)
    
    def __repr__(self):
        return (f'HTMLNode(tag="{self.tag}", value="{self.value}", '
            f'children={self.children}, props={self.props})')