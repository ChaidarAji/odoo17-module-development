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
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_deposit = fields.Boolean(related="pos_config_id.enable_deposit", readonly=False)
    deposit_product = fields.Many2one(related="pos_config_id.deposit_product", readonly=False)        
