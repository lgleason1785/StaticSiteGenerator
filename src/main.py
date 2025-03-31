from textnode import *
from enums import TextType


def main():
    test = TextNode("test", TextType.BOLD)
    print (test.__repr__())

if __name__ == "__main__":
    main()