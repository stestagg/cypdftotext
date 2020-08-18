"""Tests for the PDF class."""

import io
import pkg_resources
import unittest

import cypdftotext as pdftotext


file_names = [
    "abcde.pdf",
    "blank.pdf",
    "corrupt.pdf",
    "corrupt_page.pdf",
    "landscape_0.pdf",
    "landscape_90.pdf",
    "portrait.pdf",
    "table.pdf",
    "two_page.pdf",
]
test_files = {}
for file_name in file_names:
    file_path = pkg_resources.resource_filename("tests", file_name)
    with open(file_path, "rb") as open_file:
        test_files[file_name] = open_file.read()


def get_file(name):
    """Return a copy of the requested test file as if it were just opened."""
    return test_files[name]


class InitTest(unittest.TestCase):
    """Test using and abusing __init__."""

    def test_double_init_success(self):
        pdf = pdftotext.PDF(get_file("abcde.pdf"))
        pdf.__init__(get_file("blank.pdf"))
        self.assertEqual(len(pdf), 1)

    def test_init_file_in_text_mode(self):
        text_file = io.StringIO(u"wrong")
        with self.assertRaises(TypeError):
            pdftotext.PDF(text_file)

    def test_init_invalid_pdf_file(self):
        pdf_file = io.BytesIO(b"wrong")
        with self.assertRaises(TypeError):
            pdftotext.PDF(pdf_file)

    def test_init_corrupt_pdf_file(self):
        with self.assertRaises(ValueError):
            pdftotext.PDF(get_file("corrupt.pdf"))

    def test_no_init(self):
        class BrokenPDF(pdftotext.PDF):
            def __init__(self):
                pass

        with self.assertRaises(TypeError):
            pdf = BrokenPDF()


class IterTest(unittest.TestCase):

    def test_iter(self):
        pdf = pdftotext.PDF(get_file('two_page.pdf'))
        self.assertEqual([x.strip() for x in list(pdf)], ['one.', 'two.'])

class GetItemTest(unittest.TestCase):
    """Test the __getitem__ method."""

    def test_read(self):
        pdf = pdftotext.PDF(get_file("abcde.pdf"))
        result = pdf[0]
        self.assertIn("abcde", result)

    def test_read_portrait(self):
        pdf = pdftotext.PDF(get_file("portrait.pdf"))
        result = pdf[0]
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertIn("d", result)

    def test_read_landscape_0(self):
        pdf = pdftotext.PDF(get_file("landscape_0.pdf"))
        result = pdf[0]
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertIn("d", result)

    def test_read_landscape_90(self):
        pdf = pdftotext.PDF(get_file("landscape_90.pdf"), layout=pdftotext.TextLayout.raw, encoding='latin1')
        result = pdf[0]
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertIn("d", result)

    def test_pdf_read_invalid_page_number(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(IndexError):
            pdf[100]

    def test_pdf_read_wrong_arg_type(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        with self.assertRaises(TypeError):
            pdf["wrong"]

    def test_read_corrupt_page(self):
        with self.assertRaises(IndexError):
            pdf = pdftotext.PDF(get_file("corrupt_page.pdf"))
            pdf[0]

    def test_read_page_two(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        result = pdf[1]
        self.assertIn("two", result)


class LengthTest(unittest.TestCase):
    """Test the __len__ method."""

    def test_length_one(self):
        pdf = pdftotext.PDF(get_file("blank.pdf"))
        self.assertEqual(len(pdf), 1)

    def test_length_two(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        self.assertEqual(len(pdf), 2)


class ListTest(unittest.TestCase):
    """Test iterating over pages."""

    def test_list_length(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        self.assertEqual(len(pdf), 2)

    def test_list_first_element(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        self.assertIn("one", pdf[0])

    def test_list_second_element(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        self.assertIn("two", pdf[1])

    def test_list_invalid_element(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        with self.assertRaises(IndexError):
            pdf[2]

    def test_list_last_element(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        self.assertIn("two", pdf[-1])

    def test_for_loop(self):
        pdf = pdftotext.PDF(get_file("two_page.pdf"))
        result = ""
        for page in pdf:
            result = result + page
        self.assertIn("one", result)
        self.assertIn("two", result)


class RawTest(unittest.TestCase):
    """Test reading in raw layout."""

    def test_raw_vs_not(self):
        filename = "table.pdf"
        pdf = pdftotext.PDF(get_file(filename))
        raw_pdf = pdftotext.PDF(get_file(filename), layout=pdftotext.TextLayout.raw)
        self.assertNotEqual(pdf[0], raw_pdf[0])

    def test_raw_is_not_default(self):
        filename = "table.pdf"
        pdf_default = pdftotext.PDF(get_file(filename))
        pdf_raw_false = pdftotext.PDF(get_file(filename), layout=pdftotext.TextLayout.physical)
        self.assertEqual(pdf_default[0], pdf_raw_false[0])
