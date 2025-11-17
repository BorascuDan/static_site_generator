import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_with_multiple_attributes(self):
        node = HTMLNode(tag='a', props={'href': 'https://example.com', 'target': '_blank'})
        result = node.props_to_html()
        self.assertIn('href="https://example.com"', result)
        self.assertIn('target="_blank"', result)

    def test_props_to_html_with_single_attribute(self):
        node = HTMLNode(tag='p', props={'class': 'intro'})
        self.assertEqual(node.props_to_html(), 'class="intro"')

    def test_props_to_html_with_no_attributes(self):
        node = HTMLNode(tag='div')
        node.props = None
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_with_empty_dict(self):
        node = HTMLNode(tag='div', props={})
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_with_special_characters(self):
        node = HTMLNode(tag='img', props={'data-info': 'a&b=c', 'alt': 'weird "quote"'})
        result = node.props_to_html()
        self.assertIn('data-info="a&b=c"', result)
        self.assertIn('alt="weird "quote""', result)

    def test_repr_contains_expected_fields(self):
        node = HTMLNode(tag='span', value='Hello', props={'style': 'color:red'})
        representation = repr(node)
        self.assertIn('tag=', representation)
        self.assertIn('value=', representation)
        self.assertIn('props=', representation)
        self.assertIn('children=', representation)

    def test_repr_with_no_props_or_children(self):
        node = HTMLNode(tag='div', value='content')
        representation = repr(node)
        self.assertIn('tag=div', representation)
        self.assertIn('value=content', representation)
        self.assertIn('children=None', representation)
        self.assertIn('props=None', representation)

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag='p', value='should fail')
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_init_all_fields_assigned_correctly(self):
        props = {'id': 'main'}
        children = [HTMLNode(tag='span', value='child')]
        node = HTMLNode(tag='div', value='parent', children=children, props=props)
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, 'parent')
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)


if __name__ == '__main__':
    unittest.main()
