# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends('deposit_lines')
    def _calc_remaining(self):
        for row in self:
            total = 0.00
            for line in row.deposit_lines:
                if line.state == 'done':
                    total += line.credit - line.debit
            row.remaining_deposit_amount = total

    deposit_lines = fields.One2many('customer.deposit', 'customer_id', string="Deposits", readonly=True)
    remaining_deposit_amount = fields.Float(compute="_calc_remaining", string="Remaining Amount", readonly=True, store=False)
    add_change_deposit = fields.Boolean('Add Change to Deposit')
