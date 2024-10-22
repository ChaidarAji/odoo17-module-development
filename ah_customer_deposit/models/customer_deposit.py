# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CustomerDeposit(models.Model):
    _name = 'customer.deposit'
    _description = "Customer Deposit Management"    
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def action_done(self):
        self.state = "done"

    def action_cancel(self):
        self.state = "cancel"

    def create_from_ui(self, vals, auto_close=True):
        result = self.env['customer.deposit'].create(vals)                    
        if auto_close:
            result.action_done()
        return result

    def create_account_move(self):
        pass 

    name = fields.Char('Name', size=100)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)    
    type = fields.Selection([('change', 'Change'), ('recharge', 'Recharge')], string="Type", required=True, default="recharge")
    debit = fields.Float("Debit")
    credit = fields.Float("Credit")

    cashier_id = fields.Many2one('res.users', string='Cashier')
    order_id = fields.Many2one('pos.order', string='Order')

    state = fields.Selection([('open','Open'),('done','Close'),('cancel','Cancel')], 'Status', default="open")

    note = fields.Char(string="Note")
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('customer.deposit') or _("New")
        result = super(CustomerDeposit,self).create(vals)
        return result