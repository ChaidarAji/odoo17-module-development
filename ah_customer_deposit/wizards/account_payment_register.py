# -*- coding: utf-8 -*-
from collections import defaultdict

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import frozendict


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    
    def _create_payments(self):
        if not self.journal_id.is_deposit:
            return super(AccountPaymentRegister,self)._create_payments()

        if self.partner_id.remaining_deposit_amount >= self.amount:
            try:                
                vals = {
                    'customer_id': self.partner_id.id,
                    'type': 'change',
                    'debit': self.amount,
                    'cashier_id': self.env.user.id,
                    'note': 'Invoice :'+self.communication
                }
                res = self.env['customer.deposit'].create_from_ui(vals)        
                res.action_done()                
                return super(AccountPaymentRegister,self)._create_payments()
            except Exception as e:
                raise ValidationError(e)
        else:
            raise ValidationError('Deposit balance not sufficient')

    remaining_deposit_amount = fields.Float(related='partner_id.remaining_deposit_amount', string="Remaining Deposit Amount")
    is_deposit = fields.Boolean(related='journal_id.is_deposit')