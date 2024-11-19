# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from itertools import groupby

class PosOrder(models.Model):
    _inherit = "pos.order"

    def _create_order_picking(self):
        self.ensure_one()
        if self.shipping_date:
            if self.lines.filtered(lambda x: x.to_ship_line_qty):
                self.lines.filtered(lambda x: x.to_ship_line_qty)._launch_stock_rule_from_pos_order_lines()

            if self.lines.filtered(lambda x: x.to_ship_line_qty<abs(x.qty)):
                if self._should_create_picking_real_time():
                    picking_type = self.config_id.picking_type_id
                    if self.partner_id.property_stock_customer:
                        destination_id = self.partner_id.property_stock_customer.id
                    elif not picking_type or not picking_type.default_location_dest_id:
                        destination_id = self.env['stock.warehouse']._get_partner_locations()[0].id
                    else:
                        destination_id = picking_type.default_location_dest_id.id

                    pickings = self.env['stock.picking']._create_picking_from_pos_order_lines(destination_id,
                                                                                              self.lines.filtered(lambda x: x.to_ship_line_qty < abs(x.qty)),
                                                                                              picking_type,
                                                                                              self.partner_id)
                    pickings.write({'pos_session_id': self.session_id.id, 'pos_order_id': self.id, 'origin': self.name})
        else:
            if self._should_create_picking_real_time():
                picking_type = self.config_id.picking_type_id
                if self.partner_id.property_stock_customer:
                    destination_id = self.partner_id.property_stock_customer.id
                elif not picking_type or not picking_type.default_location_dest_id:
                    destination_id = self.env['stock.warehouse']._get_partner_locations()[0].id
                else:
                    destination_id = picking_type.default_location_dest_id.id
                pickings = self.env['stock.picking']._create_picking_from_pos_order_lines(destination_id, self.lines,
                                                                                          picking_type, self.partner_id)
                pickings.write({'pos_session_id': self.session_id.id, 'pos_order_id': self.id, 'origin': self.name})

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    to_ship_line_qty = fields.Float(string="Ship Later Qty.")

    def _launch_stock_rule_from_pos_order_lines(self):

        procurements = []
        for line in self:
            line = line.with_company(line.company_id)
            if not line.product_id.type in ('consu','product'):
                continue

            group_id = line._get_procurement_group()
            if not group_id:
                group_id = self.env['procurement.group'].create(line._prepare_procurement_group_vals())
                line.order_id.procurement_group_id = group_id

            values = line._prepare_procurement_values(group_id=group_id)
            product_qty = line.to_ship_line_qty

            procurement_uom = line.product_id.uom_id
            procurements.append(self.env['procurement.group'].Procurement(
                line.product_id, product_qty, procurement_uom,
                line.order_id.partner_id.property_stock_customer,
                line.name, line.order_id.name, line.order_id.company_id, values))
        if procurements:
            self.env['procurement.group'].run(procurements)

        # This next block is currently needed only because the scheduler trigger is done by picking confirmation rather than stock.move confirmation
        orders = self.mapped('order_id')
        for order in orders:
            pickings_to_confirm = order.picking_ids
            if pickings_to_confirm:
                # Trigger the Scheduler for Pickings
                pickings_to_confirm.action_confirm()
                tracked_lines = order.lines.filtered(lambda l: l.product_id.tracking != 'none')
                lines_by_tracked_product = groupby(sorted(tracked_lines, key=lambda l: l.product_id.id), key=lambda l: l.product_id.id)
                for product_id, lines in lines_by_tracked_product:
                    lines = self.env['pos.order.line'].concat(*lines)
                    moves = pickings_to_confirm.move_ids.filtered(lambda m: m.product_id.id == product_id)
                    moves.move_line_ids.unlink()
                    moves._add_mls_related_to_order(lines, are_qties_done=False)
                    moves._recompute_state()
        return True