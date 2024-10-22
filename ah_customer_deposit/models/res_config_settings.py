# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_deposit = fields.Boolean(related="pos_config_id.enable_deposit", readonly=False)
    deposit_product = fields.Many2one(related="pos_config_id.deposit_product", readonly=False)        
