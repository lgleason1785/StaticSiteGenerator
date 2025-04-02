from enums import BlockType
import re

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
