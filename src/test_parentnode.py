import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    def test_to_html_with_single_child(self):
        """ParentNode cu un singur copil LeafNode"""
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span>text</span></div>")

    def test_to_html_with_multiple_children(self):
        """ParentNode cu mai mulți copii LeafNode"""
        children = [
            LeafNode("p", "Hello"),
            LeafNode("b", "World"),
        ]
        parent = ParentNode("div", children)
        self.assertEqual(parent.to_html(), "<div><p>Hello</p><b>World</b></div>")

    def test_to_html_with_nested_parents(self):
        """ParentNode imbricat în alt ParentNode"""
        inner = ParentNode("span", [LeafNode("i", "italic")])
        outer = ParentNode("div", [inner])
        self.assertEqual(outer.to_html(), "<div><span><i>italic</i></span></div>")

    def test_to_html_with_props(self):
        """ParentNode cu atribute HTML"""
        child = LeafNode("span", "content")
        parent = ParentNode("div", [child], {"class": "wrapper", "id": "main"})
        self.assertIn('<div class="wrapper" id="main">', parent.to_html())
        self.assertTrue(parent.to_html().endswith("</div>"))

    def test_to_html_with_empty_props(self):
        """ParentNode cu props gol"""
        child = LeafNode("p", "text")
        parent = ParentNode("div", [child], {})
        self.assertEqual(parent.to_html(), "<div><p>text</p></div>")

    def test_init_without_tag(self):
        """Aruncă eroare dacă tag-ul e None"""
        child = LeafNode("span", "child")
        with self.assertRaises(Exception):
            ParentNode(None, [child])

    def test_init_without_children(self):
        """Aruncă eroare dacă children e None"""
        with self.assertRaises(Exception):
            ParentNode("div", None)

    def test_to_html_missing_tag(self):
        """Aruncă ValueError dacă tag-ul lipsește"""
        child = LeafNode("p", "text")
        node = ParentNode("div", [child])
        node.tag = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_missing_children(self):
        """Aruncă ValueError dacă children e None"""
        node = ParentNode("div", [LeafNode("p", "t")])
        node.children = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_children_list(self):
        """Returnează tag gol dacă lista de copii e goală"""
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_to_html_with_mixed_children(self):
        """ParentNode care are atât LeafNode cât și ParentNode copii"""
        nested = ParentNode("ul", [LeafNode("li", "Item 1"), LeafNode("li", "Item 2")])
        parent = ParentNode("div", [
            LeafNode("h1", "Title"),
            nested,
            LeafNode("p", "Description")
        ])
        self.assertEqual(
            parent.to_html(),
            "<div><h1>Title</h1><ul><li>Item 1</li><li>Item 2</li></ul><p>Description</p></div>"
        )

    def test_to_html_with_deep_nesting(self):
        """ParentNode adânc imbricat (recursivitate)"""
        level3 = ParentNode("b", [LeafNode(None, "text")])
        level2 = ParentNode("i", [level3])
        level1 = ParentNode("span", [level2])
        parent = ParentNode("div", [level1])
        self.assertEqual(parent.to_html(), "<div><span><i><b>text</b></i></span></div>")

    def test_to_html_with_text_leaf(self):
        """ParentNode care conține un LeafNode fără tag (doar text)"""
        text_node = LeafNode(None, "plain text")
        parent = ParentNode("div", [text_node])
        self.assertEqual(parent.to_html(), "<div>plain text</div>")

if __name__ == "__main__":
    unittest.main()
