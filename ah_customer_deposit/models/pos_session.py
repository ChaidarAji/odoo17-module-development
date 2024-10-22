# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api
from odoo.tools import float_is_zero, float_round
from odoo.exceptions import UserError, ValidationError


import logging
_logger = logging.getLogger(__name__)

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_pos_payment_method(self):
        result = super()._loader_params_pos_payment_method()
        result['search_params']['fields'].append('terminal_id')               
        return result

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].append('remaining_deposit_amount')               
        return result