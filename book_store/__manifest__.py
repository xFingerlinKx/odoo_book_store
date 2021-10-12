# -*- coding: utf-8 -*-
{
    'name': "Book Store",

    'summary': """Book Store""",

    'description': """Book store application""",

    'author': "Artur Apanasov",

    'license': "AGPL-3",

    'depends': ['product'],

    'application': True,

    'installable': True,

    'data': [

        'security/ir.model.access.csv',

        'views/book_store_menu.xml',
        'views/product_template_ext_book_view.xml',
        'views/res_partner_ext.xml',

        'templates/book_pages_template.xml',

        'wizard/add_new_store_book_wizard_view.xml',
    ],
}