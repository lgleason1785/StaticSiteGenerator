import re

from textnode import TextNode
from enums import TextType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    #Apply each transformation
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

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

def extract_markdown_links(markdown):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, markdown)
    return matches

def extract_markdown_images(markdown):
    regex =  r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, markdown)
    return matches