# 1 : imports of python lib
import logging

# 2 :  imports of odoo
from odoo import api, fields, models, _

# 3 :  imports of odoo modules

# 4 :  imports from custom modules
from .. import constants


_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """
    Partner Model Extension For Book Store
    """

    # Private attributes
    # ------------------------------------------------------------------------------------------------------------------
    _inherit = 'res.partner'
    _order = "name asc"

    # Default methods
    # ------------------------------------------------------------------------------------------------------------------

    # Fields declaration
    # ------------------------------------------------------------------------------------------------------------------

    partner_type = fields.Selection(
        string='Partner Type',
        selection=constants.RES_PARTNER_TYPES,
        default=constants.RES_PARTNER_AUTHOR,
    )
    """ Partner Type - author or publisher """

    published_book_ids = fields.Many2many(
        string='Published Books',
        comodel_name='product.template',
        relation='product_template_partner_publisher_rel',
        column1='partner_id',
        column2='product_id',
    )
    """ Published Books """

    authored_book_ids = fields.Many2many(
        string='Authored Books',
        comodel_name='product.template',
        relation='product_template_partner_authors_rel',
        column1='author_id',
        column2='product_id',
    )
    """ Authored Books """

    # Default methods
    # ------------------------------------------------------------------------------------------------------------------
    #
    # Selection method (methods used to return computed values for selection fields)
    # ------------------------------------------------------------------------------------------------------------------

    # Compute and search fields, in the same order of fields declaration
    # ------------------------------------------------------------------------------------------------------------------

    # Constraints and onchanges
    # ------------------------------------------------------------------------------------------------------------------

    # Business methods
    # ------------------------------------------------------------------------------------------------------------------

    def _get_or_create_partner_by_name_and_type(self, name, partner_type):
        """
        The method decides whether to create a new res.partner record
        if the partner does not exist or returns an existing records.

        :param name: {str} name of res.partner
        :param partner_type: {str} type of res.partner ('is_author' or 'is_publisher')
        :return: {list} authors and publishers res.partner objects
        """
        partners_objects = []
        names = name.split(', ')
        for name in names:
            query = """
                        SELECT id
                        FROM res_partner
                        WHERE name LIKE '{name}'
                            AND partner_type = '{partner_type}'
            """.format(**{
                'name': name,
                'partner_type': partner_type
            })
            self.env.cr.execute(query)
            partners_ids = [row[0] for row in self.env.cr.fetchall()]

            if not partners_ids:
                partner = self.create({'name': name, 'partner_type': partner_type, 'title': 0})
                partners_objects.append(partner)
                continue
            else:
                partners_objects.extend(self.browse(partners_ids))
        return partners_objects

    # CRUD methods
    # ------------------------------------------------------------------------------------------------------------------

    # Action methods
    # ------------------------------------------------------------------------------------------------------------------

    # And finally, other business methods.
    # ------------------------------------------------------------------------------------------------------------------
