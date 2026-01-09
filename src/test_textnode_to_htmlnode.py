import unittest
from textnode import TextNode, TextType
from textnode_to_htmlnode import text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_bold(self):
        node = TextNode("Bold", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.value, "Bold")

    def test_link(self):
        node = TextNode("Google", TextType.LINK, "https://google.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.props["href"], "https://google.com")

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "img.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.props["src"], "img.png")
        self.assertEqual(html.props["alt"], "Alt text")

    def test_unknown_type(self):
        # On crée un type qui n'existe normalement pas ou une erreur de type intentionnelle
        node = TextNode("Oups", "unknown_type") 
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    if __name__ == "__main__":
        unittest.main()