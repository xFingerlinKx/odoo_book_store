# 1 : imports of python lib
import logging
import requests
import base64

# 2 :  imports of odoo
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

# 3 :  imports of odoo modules

# 4 :  imports from custom modules
# noinspection PyUnresolvedReferences
from odoo.addons.book_store.tools.api_service import ApiService
from ..utils import check_is_isbn_valid
from .. import constants


_logger = logging.getLogger(__name__)


class AddNewStoreBookWizard(models.TransientModel):
    _name = 'add_new.store_book.wizard'

    # Default methods
    # ------------------------------------------------------------------------------------------------------------------

    # Fields declaration
    # ------------------------------------------------------------------------------------------------------------------

    isbn = fields.Char(
        string='ISBN',
        required=True,
    )
    """ ISBN number """

    title = fields.Char(
        string='Book Title',
    )
    """ Book Title """

    authors = fields.Char(
        string='Book Authors',
    )
    """ Book Authors """

    publishers = fields.Char(
        string='Book Publishers',
    )
    """ Book Publishers """

    page_qty = fields.Integer(
        string='Number Of The Book Pages',
    )
    """ Number Of The Book Pages """

    date_published = fields.Char(
        string='Year of book released',
    )
    """ Year of book released """

    book_cover = fields.Binary(
        string='Book Cover',
    )
    """ Book Cover """

    # Default methods
    # ------------------------------------------------------------------------------------------------------------------
    #
    # Selection method (methods used to return computed values for selection fields)
    # ------------------------------------------------------------------------------------------------------------------

    # Compute and search fields, in the same order of fields declaration
    # ------------------------------------------------------------------------------------------------------------------

    # Constraints and onchanges
    # ------------------------------------------------------------------------------------------------------------------

    @api.constrains('isbn')
    def constrains_is_isbn_valid(self):
        """
        Checks for ISBN-10 or ISBN-13 format.
        """
        for book in self:
            check_is_isbn_valid(book.isbn)

    # Business methods
    # ------------------------------------------------------------------------------------------------------------------

    @api.model
    def get_service_for_get_response(self, env):
        """
        Get API service to make Bool API request and get response.

        :param env: {odoo.api.Environment} environment object
        :return: {api_service.ApiService} API service object
        """
        return ApiService(env)

    def _parse_response_data(self, response_data):
        """
        Get data for books from response data.

        :param response_data: {dict} response_data
        :return: {dict} book data
        """
        if not response_data:
            raise ValidationError(_('There is no response data! Try latter.'))
        return {
            'isbn': self.isbn,
            'title': response_data.get('title', ''),
            'publishers': self._get_publishers_from_response_data(response_data),
            'authors': self._get_authors_from_response_data(response_data),
            'page_qty': response_data.get('number_of_pages'),
            'date_published': self._get_book_published_year_from_response_data(response_data),
            'book_cover': self._get_image_from_response_data_url(response_data),
        }

    @staticmethod
    def _get_publishers_from_response_data(response_data):
        """
        Get publishers names from list of dicts (key=name)
        and concatenate in one string with comma.

        :param response_data: {dict} response_data
        :return: {str} book publishers
        """
        return ', '.join([publisher_name.get('name') for publisher_name in response_data.get('publishers', [])])

    @staticmethod
    def _get_authors_from_response_data(response_data):
        """
        Get publishers names from list of dicts (key=name)
        and concatenate in one string with comma.

        :param response_data: {dict} response_data
        :return: {str} book authors
        """
        return ', '.join([publisher_name.get('name') for publisher_name in response_data.get('authors', [])])

    @staticmethod
    def _get_image_from_response_data_url(response_data, book_cover_size=constants.BOOK_COVER_SIZE_MEDIUM):
        """
        Get book cover URL and then get binary data of this cover.
        It is possible to choose the cover image size.

        :param response_data: {dict} response_data
        :param book_cover_size: {str} cover image size types
        :return: {base64} book cover image
        """
        book_url = (response_data.get('cover').get(book_cover_size))
        return base64.b64encode(requests.get(book_url.strip()).content).replace(b'\n', b'')

    @staticmethod
    def _get_book_published_year_from_response_data(response_data):
        """
        Get book published year from response string data.

        :param response_data: {dict} response_data
        :return: {str} book published year
        """
        book_published_date_str = response_data.get('publish_date')
        if not book_published_date_str:
            return ''
        return book_published_date_str.split(', ')[1] \
            if len(book_published_date_str.split(', ')) > 1 \
            else book_published_date_str.split(', ')[0]

    def _get_or_create_new_partner(self, name, partner_type):
        """
        The method decides whether to create a new res.partner record
        if the partner does not exist or returns an existing records.

        :param name: {str} name of res.partner
        :param partner_type: {str} type of res.partner ('is_author' or 'is_publisher')
        :return: {list} authors and publishers res.partner objects
        """
        # noinspection PyProtectedMember
        return self.env['res.partner']._get_or_create_partner_by_name_and_type(name=name, partner_type=partner_type)

    def add_new_store_book(self, context):
        """
        Create and return new 'product.template' record (book).

        :param context: {dict} new book values
        :return: {product.template} new book record
        """
        # noinspection PyProtectedMember
        return self.env['product.template']._create_new_store_book_from_data(context)

    def _update_book_data(self, book_data):
        """
        Update the book data if the user change something from the wizard window.

        :param book_data: {odoo.tools.misc.frozendict} environment context object
        :return: {dict} new book values
        """
        data = dict(book_data)
        list_of_field_names = ['isbn', 'title', 'publishers', 'authors', 'page_qty', 'date_published', 'book_cover']
        for field_name in list_of_field_names:
            if data['default_' + field_name] != self[field_name]:
                data['default_' + field_name] = self[field_name]
        return data

        # CRUD methods
    # ------------------------------------------------------------------------------------------------------------------

    # Action methods
    # ------------------------------------------------------------------------------------------------------------------

    def action_get_response_data(self):
        """
        Action wizard method to make request and get response with book data.
        After getting data it open the next action view and put data to it in the context.

        :return: {ir.actions.act_window} next wizard view
        """
        response_data = {}
        service = self.get_service_for_get_response(self.env)
        response_content_dict, response_error_log = service.get_book_api_response(self.isbn)
        if response_error_log:
            raise ValidationError(response_error_log)
        if response_content_dict:
            response_data = response_content_dict.get(f'ISBN:{self.isbn}')

        book_data = self._parse_response_data(response_data)

        if book_data:
            return {
                'name': _('Added Book'),
                'type': 'ir.actions.act_window',
                'res_model': 'add_new.store_book.wizard',
                'view_mode': 'form',
                'view_id': self.env.ref('book_store.add_new_store_book_wizard_step_2_view').id,
                'target': 'new',
                'context': {
                    'default_isbn': book_data.get('isbn'),
                    'default_title': book_data.get('title'),
                    'default_publishers': book_data.get('publishers'),
                    'default_authors': book_data.get('authors'),
                    'default_page_qty': book_data.get('page_qty'),
                    'default_date_published': book_data.get('date_published'),
                    'default_book_cover': book_data.get('book_cover'),
                },
            }

    def action_create_store_book_data(self):
        """
        Action wizard method that get book data from the context,
        check if it need to be updated and add and link new book, authors and publishers to the store.
        :return: {ir.actions.client} the result - new book and reload the page to show new created records
        """
        book_data = self._update_book_data(self.env.context)

        publishers = self._get_or_create_new_partner(
            name=book_data['default_publishers'],
            partner_type=constants.RES_PARTNER_PUBLISHER
        )

        authors = self._get_or_create_new_partner(
            name=book_data['default_authors'],
            partner_type=constants.RES_PARTNER_AUTHOR
        )

        book_data = self._update_book_data(self.env.context)
        book = self.add_new_store_book(book_data)

        is_book_created = book.write({
            'publisher_ids': [(6, 0, [publisher.id for publisher in publishers])],
            'author_ids': [(6, 0, [author.id for author in authors])],
        })

        if not is_book_created:
            raise ValidationError(_('Something went wrong!'))

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    # And finally, other business methods.
    # ------------------------------------------------------------------------------------------------------------------
