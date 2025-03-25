from leafnode import LeafNode
from textnode import TextType

def text_node_to_html_node(text_node):
    if text_node.text is None and text_node.text_type != TextType.IMAGE:
        raise ValueError("TextNode value cannot be None for non-IMAGE types.")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
             return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url is None or text_node.url == "":
                raise ValueError("TextNode of type LINK must have a valid url.")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None or text_node.url == "":
                raise ValueError("TextNode of type IMAGE must have a valid url.")
            return LeafNode("img", "", {"src": text_node.url ,"alt": text_node.text})
        case _:
            raise TypeError("unexpected text type")