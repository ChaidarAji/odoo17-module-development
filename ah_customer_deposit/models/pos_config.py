# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


import logging
_logger = logging.getLogger(__name__)

class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_deposit = fields.Boolean('Enable Deposit')
    deposit_product = fields.Many2one('product.product', string="Deposit Product")    