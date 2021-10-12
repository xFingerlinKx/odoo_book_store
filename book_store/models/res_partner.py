# 1 : imports of python lib
import logging

# 2 :  imports of odoo
from odoo import api, fields, models, _

# 3 :  imports of odoo modules

# 4 :  imports from custom modules
from .. import constants


class ResPartnerExt(models.Model):
    """
    Расширение модели res.partner
    """

    # Private attributes
    # ------------------------------------------------------------------------------------------------------------------
    _inherit = 'res.partner'
    _order = 'name asc'

    # Default methods
    # ------------------------------------------------------------------------------------------------------------------

    # Fields declaration
    # ------------------------------------------------------------------------------------------------------------------

    firstname = fields.Char(
        string="Имя",
    )
    """ Имя """
