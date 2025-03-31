import re
from leafnode import LeafNode
from textnode import TextNode
from enums import *

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

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    #Apply each transformation
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def extract_markdown_images(markdown):
    regex =  r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, markdown)
    return matches

def extract_markdown_links(markdown):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, markdown)
    return matches

def split_nodes_link(old_nodes):
    new_nodes = [] 
    for node in old_nodes: #Iterate through nodes
        if node.text_type != TextType.TEXT: #If not an image node
            new_nodes.append(node) #Just add to list
            continue
        
        #Extract link from markdown in node
        links = extract_markdown_links(node.text)

        if links == []: #If no link found in node
            new_nodes.append(node) #Just add to list
            continue

        #Process links one at a time
        remaining_text = node.text

        for anchor, url in links:
            #Find location of image markdown in text
            link_markdown = f"[{anchor}]({url})"
            parts = remaining_text.split(link_markdown, 1)

            #Add a text node for the part before the image
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            #Add the link node
            new_nodes.append(TextNode(anchor, TextType.LINK, url))

            #Update remaining text to be part after link
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        #Add any remaining text after all links are processed
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = [] 
    for node in old_nodes: #Iterate through nodes
        if node.text_type != TextType.TEXT: #If not an image node
            new_nodes.append(node) #Just add to list
            continue
        
        #Extract image from markdown in node
        images = extract_markdown_images(node.text)

        if images == []: #If no images found in node
            new_nodes.append(node) #Just add to list
            continue

        #Process images one at a time
        remaining_text = node.text

        for alt, url in images:
            #Find location of image markdown in text
            image_markdown = f"![{alt}]({url})"
            parts = remaining_text.split(image_markdown, 1)

            #Add a text node for the part before the image
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            #Add the image node
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            #Update remaining text to be part after image
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        #Add any remaining text after all images are processed
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes: #Iterate through nodes
        if node.text_type != TextType.TEXT: #If not Text 
            new_nodes.append(node) #Just append node to list
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
     
        #Split by delimiter
        parts = node.text.split(delimiter)

        #Check for paired delimiters
        if len(parts) % 2 == 0:
            #Odd number of delimiters, invalid markdown
            raise ValueError(f"Invalid markdown: missing closing '{delimiter}'")
            
        #Process parts
        inside_delimiter = False
        for part in parts:
            if part == "":
                inside_delimiter = not inside_delimiter #Maintain toggle state
                continue 

            if inside_delimiter:
                new_nodes.append(TextNode(part, text_type))
                inside_delimiter = False
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))
                inside_delimiter = True
    
    return new_nodes
    
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    #Create  a new list of non-empty blocks
    clean_blocks = []

    #Iterate through blocks
    for block in blocks:
        #Split block into lines, strip each line, then join
        lines = block.split("\n")
        stripped_lines = [line.strip() for line in lines]
        clean_block = "\n".join(stripped_lines).strip()

        if clean_block != "": #Only add non-empty blocks
            clean_blocks.append(clean_block)
    
    return clean_blocks
    
def block_to_block_type(block):
    if re.match(r"(^#{1,6})\s", block): #Matches Heading Block
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"): #Matches Code Block
        return BlockType.CODE
    
    #Prepare to check line based blocks
    lines = block.split("\n")
    
    if all(line.startswith(">") for line in lines): #Matches Quote blocks
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines): #Matches Unordered List blocks
        return BlockType.UNORDERED_LIST
    
    #Matches ordered list blocks
    expected_number = 1
    for line in lines:
        match = re.match(r"^(\d+)\.\s", line)
        if match:
            number = int(match.group(1))
            if number != expected_number: #Checks to see if incremented correctly
                break
            expected_number += 1
        else:
            break
    else:
        #Above loops only completes if all lines are validated as an ordered list
        return BlockType.ORDERED_LIST
    
    #Default to paragraph if no other types found
    return BlockType.PARAGRAPH
    