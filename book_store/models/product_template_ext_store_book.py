# 1 : imports of python lib
import logging
import re

# 2 :  imports of odoo
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

# 3 :  imports of odoo modules

# 4 :  imports from custom modules
from .. import constants
from ..utils import check_is_isbn_valid


_logger = logging.getLogger(__name__)


class ProductTemplateExtBook(models.Model):
    """
    Product Template Model Extension For Book Store
    """

    # Private attributes
    # ------------------------------------------------------------------------------------------------------------------

    _inherit = 'product.template'
    _order = "name asc"

    # Default methods
    # ------------------------------------------------------------------------------------------------------------------

    # Fields declaration
    # ------------------------------------------------------------------------------------------------------------------

    isbn = fields.Char(
        string='ISBN',
        required=True,
        index=True,
    )
    """ ISBN number """

    publisher_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='product_template_partner_publisher_rel',
        column1='product_id',
        column2='partner_id',
        string='Publishers',
    )
    """ Publishers """

    author_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='product_template_partner_authors_rel',
        column1='product_id',
        column2='author_id',
        string='Authors',
    )
    """ Authors """

    date_published = fields.Char(
        string='Publish Date',
        size=4,
    )
    """ Year of book released """

    page_qty = fields.Integer(
        string='Number Of Pages',
    )
    """ Number Of Pages """

    reference_field = fields.Char(
        string='Reference',
        compute='_compute_reference_field',
        store=True,
    )

    # Compute and search fields, in the same order of fields declaration
    # ------------------------------------------------------------------------------------------------------------------

    @api.depends('isbn', 'author_ids', 'name', 'date_published')
    def _compute_reference_field(self):
        for book in self:
            book.reference_field = f'[{book.isbn}] ' \
                                   f'{self.get_authors_name_str(book.author_ids)} - ' \
                                   f'{book.name} ' \
                                   f'({book.date_published})'

    # Selection method (methods used to return computed values for selection fields)
    # ------------------------------------------------------------------------------------------------------------------

    # Constraints and onchanges
    # ------------------------------------------------------------------------------------------------------------------

    @api.constrains('isbn')
    def constrains_is_isbn_unique(self):
        """
        ISBN must be unique.
        """
        for book in self:
            is_isbn_not_unique = self.env['product.template'].search_count([
                ('isbn', '=', book.isbn),
                ('id', '!=', book.id),
            ])
            if is_isbn_not_unique:
                raise ValidationError(_(constants.ISBN_IS_NOT_UNIQUE_MSG))

    @api.constrains('isbn')
    def constrains_is_isbn_valid(self):
        """
        Checks for ISBN-10 or ISBN-13 format.
        """""
        for book in self:
            check_is_isbn_valid(book.isbn)

    @api.constrains('page_qty')
    def constraint_is_page_qty_not_negative(self):
        for book in self:
            if book.page_qty <= 0:
                raise ValidationError(_(constants.PAGE_QTY_BELLOW_ZERO_MSG))

    # Business methods
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_authors_name_str(authors):
        """
        Helper method - get string with comma separated book authors names.

        :param authors: {res.partner} book authors records
        :return: {str} book authors
        """
        if not authors:
            return constants.NO_AUTHORS_SELECTED_MESSAGE
        return ', '.join([author.name for author in authors if author.name is not False])

    @api.model
    def _create_new_store_book_from_data(self, data):
        if not data:
            raise ValidationError(_('Something wrong with book data!\n Impossible to add book!'))

        book_vals_dict = {
            'isbn': data.get('default_isbn'),
            'name': data.get('default_title'),
            'page_qty': data.get('default_page_qty'),
            'date_published': data.get('default_date_published'),
            'image_1920': data.get('default_book_cover'),
        }
        return self.create(book_vals_dict)

    # CRUD methods
    # ------------------------------------------------------------------------------------------------------------------

    # Action methods
    # ------------------------------------------------------------------------------------------------------------------

    # And finally, other business methods.
    # ------------------------------------------------------------------------------------------------------------------
