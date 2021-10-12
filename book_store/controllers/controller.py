# 1 : imports of python lib
import logging
from odoo import http
from odoo.http import request

# 2 :  imports of odoo

# 3 :  imports of odoo modules

# 4 :  imports from custom modules


_logger = logging.getLogger(__name__)


class BooksController(http.Controller):
    """
    Controller class to render books page
    """

    @http.route(['/books'], type='http', auth='public', website=True)
    def books_page(self):
        books = request.env['product.template'].sudo().search([])
        return request.render("book_store.books_page", {'books': books})

    @http.route(
        ['/books/details/<model("product.template"):book>'],
        type='http',
        auth='public',
        website=True
    )
    def render_book_details(self, book):
        return request.render("book_store.book_details", {'book': book})
