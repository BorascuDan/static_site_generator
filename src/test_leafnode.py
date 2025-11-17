import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_with_props(self):
        node = LeafNode("a", "Click here", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click here</a>')

    def test_leaf_multiple_props(self):
        node = LeafNode("img", "Image", {"src": "pic.jpg", "alt": "A picture"})
        expected = '<img src="pic.jpg" alt="A picture">Image</img>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_empty_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_empty_string_value(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_custom_tag(self):
        node = LeafNode("span", "inline text")
        self.assertEqual(node.to_html(), "<span>inline text</span>")

    def test_leaf_with_numeric_value(self):
        node = LeafNode("p", "123")
        self.assertEqual(node.to_html(), "<p>123</p>")

    def test_leaf_with_boolean_tag(self):
        node = LeafNode(None, "True")
        self.assertEqual(node.to_html(), "True")


if __name__ == "__main__":
    unittest.main()
