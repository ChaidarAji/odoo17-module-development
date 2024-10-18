# -*- coding: utf-8 -*-
#################################################################################
# Author      : WEHA Consultant (<www.ah-id.com>)
# Copyright(c): 2015-Present WEHA Consultant.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_round



import logging
_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'


    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['is_deposit_order'] = ui_order.get('is_deposit_order', False)
        return order_fields
    
    @api.model
    def _process_order(self, order, draft, existing_order):
        order_id = super(PosOrder, self)._process_order(order, draft, existing_order)
        if order_id:
            pos_order_id = self.browse(order_id)
            if pos_order_id.is_deposit_order:
                deposit_line = pos_order_id.lines.filtered(lambda p: p.product_id == pos_order_id.config_id.deposit_product)
                vals = {
                    'customer_id': pos_order_id.partner_id.id,
                    'type': 'recharge',
                    'order_id': pos_order_id.id,
                    'cashier_id': order['data']['user_id'],
                    'credit': deposit_line.price_subtotal_incl,
                    'note': "%s: %s"%(pos_order_id.picking_type_id.warehouse_id.name, pos_order_id.name)
                }
                res = self.env['customer.deposit'].create_from_ui(vals)
        return order_id
    
    is_deposit_order = fields.Char('Is Deposit Order')

   