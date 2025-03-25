from htmlnode import HTMLNode

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