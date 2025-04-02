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
        raise NotImplementedError("to_html method not implemented")
    
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

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return self.value
        props_str = self.props_to_html()
        return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None:
            raise ValueError("ParentNode must have children")
        
        #Convert props to html format
        props_str = self.props_to_html()

        #Map to_html to each child in parent's children
        #join result to single string without seperator
        children_html = "".join(map(lambda child: child.to_html(), self.children))
        
        return f'<{self.tag}{props_str}>{children_html}</{self.tag}>'

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
