# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


import logging
_logger = logging.getLogger(__name__)

class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'


    def _get_payment_terminal_selection(self):
        return super(PosPaymentMethod, self)._get_payment_terminal_selection() + [('deposit', 'Deposit')]
    
    @api.onchange('use_payment_terminal')
    def _onchange_use_payment_terminal(self):
        super(PosPaymentMethod, self)._onchange_use_payment_terminal()
        if self.use_payment_terminal != 'deposit':
            self.terminal_id = False

    terminal_id = fields.Char('Terminal #')

