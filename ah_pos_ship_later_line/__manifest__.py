# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
######################################################################################################
#
#   @author Chaidar Aji Nugroho <chaidaraji@gmail.com>
{
    'name': 'Pos Ship Later Orderline',
    'version': '17.0.0.0.1',
    'category': 'Sales',
    'description': """Add pop up form to accomodate ship later per orderline on PoS""",
    'sequence': '100',
    'website': '',
    'author': 'chaidaraji@gmail.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'point_of_sale',
    ],
    'demo': [],
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/sequence.xml',
        'views/pos_order_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'ah_pos_ship_later_line/static/src/xml/ShipLaterLinePopup.xml',
            'ah_pos_ship_later_line/static/src/xml/payment_screen.xml',
            'ah_pos_ship_later_line/static/src/js/models.js',
            'ah_pos_ship_later_line/static/src/js/PaymentScreen.js',
            'ah_pos_ship_later_line/static/src/js/ShipLaterLinePopup.js',
        ]
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
#
######################################################################################################
