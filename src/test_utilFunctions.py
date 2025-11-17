import unittest

from utilFunctions import text_node_to_html_node, split_nodes_delimitor
from src.textnode import TextType, TextNode

class TestUtilFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimitor([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    # def test_no_delimiters(self):
    #     node = TextNode("Plain text", TextType.TEXT)
    #     result = split_nodes_delimitor([node])
    #     self.assertEqual(result, [node])

    def test_single_code_block(self):
        node = TextNode("Text with `code` inside", TextType.TEXT)
        result = split_nodes_delimitor([node])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" inside", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    # def test_single_bold_block(self):
    #     node = TextNode("This is **bold** text", TextType.TEXT)
    #     result = split_nodes_delimitor([node])
    #     expected = [
    #         TextNode("This is ", TextType.TEXT),
    #         TextNode("bold", TextType.BOLD),
    #         TextNode(" text", TextType.TEXT),
    #     ]
    #     self.assertEqual(result, expected)

    def test_single_italic_block(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimitor([node])
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_text_between_delimiters(self):
        node = TextNode("Empty `` code", TextType.TEXT)
        result = split_nodes_delimitor([node])
        expected = [
            TextNode("Empty ", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode(" code", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_starting_with_delimiter(self):
        node = TextNode("`start` middle end", TextType.TEXT)
        result = split_nodes_delimitor([node])
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("start", TextType.CODE),
            TextNode(" middle end", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_ending_with_delimiter(self):
        node = TextNode("Start middle `end`", TextType.TEXT)
        result = split_nodes_delimitor([node])
        expected = [
            TextNode("Start middle ", TextType.TEXT),
            TextNode("end", TextType.CODE),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    # def test_multiple_same_type_delimiters(self):
    #     node = TextNode("`code1``code2`", TextType.TEXT)
    #     result = split_nodes_delimitor([node])
    #     expected = [
    #         TextNode("", TextType.TEXT),
    #         TextNode("code1", TextType.CODE),
    #         TextNode("", TextType.TEXT),
    #         TextNode("code2", TextType.CODE),
    #         TextNode("", TextType.TEXT),
    #     ]
    #     self.assertEqual(result, expected)

    # def test_multiple_different_delimiters(self):
    #     node = TextNode("Mix **bold** and _italic_ plus `code`", TextType.TEXT)
    #     result = split_nodes_delimitor([node])
    #     expected = [
    #         TextNode("Mix ", TextType.TEXT),
    #         TextNode("bold", TextType.BOLD),
    #         TextNode(" and ", TextType.TEXT),
    #         TextNode("italic", TextType.ITALIC),
    #         TextNode(" plus ", TextType.TEXT),
    #         TextNode("code", TextType.CODE),
    #     ]
    #     self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises(self):
        node = TextNode("Text with `unmatched code", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimitor([node])

    def test_empty_input(self):
        result = split_nodes_delimitor([])
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
