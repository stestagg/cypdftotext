# distutils: language = c++

from libcpp.string cimport string
from libcpp.vector cimport vector


cdef extern from 'poppler/cpp/poppler-version.h':
    cdef const int POPPLER_VERSION_MAJOR
    cdef const int POPPLER_VERSION_MINOR

cdef extern from 'poppler/cpp/poppler-version.h' namespace 'poppler':
    string version_string()

cdef extern from 'poppler/cpp/poppler-global.h' namespace 'poppler':
    cdef enum page_box_enum:
        media_box
        crop_box
        bleed_box
        trim_box
        art_box

    cdef cppclass rectf:
        rectf()

    cdef cppclass ustring:
        string to_latin1()
        vector[char] to_utf8()


cdef extern from 'poppler/cpp/poppler-document.h' namespace 'poppler':
    cdef cppclass document:
        @staticmethod
        document *load_from_raw_data(const char *, int)

        int pages()
        page *create_page(int)


cdef extern from 'poppler/cpp/poppler-page.h' namespace 'poppler':

    cdef cppclass page:
        rectf page_rect()
        ustring text(rectf &rect, text_layout_enum layout_mode)

        
cdef extern from 'poppler/cpp/poppler-page.h' namespace 'poppler::page':
    cdef enum text_layout_enum:
        physical_layout
        raw_order_layout
        non_raw_non_physical_layout

POPPLER_VERSION = version_string()


class TextLayout:
    physical = text_layout_enum.physical_layout
    raw = text_layout_enum.raw_order_layout
    non_raw_non_physical = NotImplemented


if POPPLER_VERSION_MAJOR > 0 or POPPLER_VERSION_MINOR >= 88:
    # This is a new enum value that will not be generally 
    # available until some point far in the future (written 2020)
    TextLayout.non_raw_non_physical = 2


cdef class PageIter:
    cdef PDF pdf
    cdef int page_num

    def __cinit__(self, pdf):
        self.pdf = pdf
        self.page_num = 0

    def __next__(self):
        cdef int cur_page = self.page_num
        if cur_page == self.pdf.num_pages:
            raise StopIteration()
        self.page_num += 1
        return self.pdf[cur_page]


cdef class PDF:

    cdef bytes data
    cdef document *doc
    cdef readonly int num_pages
    cdef text_layout_enum layout
    cdef readonly str encoding
    
    def __cinit__(self, bytes data, layout=TextLayout.physical, encoding='utf8'):
        self.data = data
        self.layout = layout
        self.encoding = encoding
        
        self.doc = document.load_from_raw_data(self.data, len(data))
        if self.doc == NULL:
            raise ValueError("Unable to read PDF")
        self.num_pages = self.doc.pages()

    def __len__(self):
        return self.num_pages

    def __iter__(self):
        return PageIter(self)

    def __getitem__(self, int page_num):
        adjusted_num = page_num
        if adjusted_num < 0:
            adjusted_num += self.num_pages
        if adjusted_num < 0 or adjusted_num >= self.num_pages:
            raise IndexError(f'Page {page_num} out of range for pdf with {self.num_pages} pages')
        cdef page *page = self.doc.create_page(adjusted_num)
        if page == NULL:
            raise ValueError(f"Error reading page {page_num}")
        cdef ustring page_text = page.text(rectf(), self.layout)
        cdef bytes page_bytes = page_text.to_latin1()
        if page_bytes[-1] == 0x0c:
            page_bytes = page_bytes[:-1]
        del page
        return page_bytes.decode(self.encoding)
