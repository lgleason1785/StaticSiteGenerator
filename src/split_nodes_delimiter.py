from textnode import TextType, TextNode

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