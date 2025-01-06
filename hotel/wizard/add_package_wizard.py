from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AddPackageWizard(models.TransientModel):
    _name = "add.package.wizard"
    _description = "Add Package Wizard"

    folio_id = fields.Many2one("hotel.folio", string="Folio")
    package_id = fields.Many2one("hotel.room.package", string="Package")
    checkin_date = fields.Datetime(string="Check In", required=True)
    checkout_date = fields.Datetime(string="Check Out", required=True)
    room_line_ids = fields.One2many("add.package.wizard.room.line", "wizard_id", string="Rooms Type")
    service_line_ids = fields.One2many("add.package.wizard.service.line", "wizard_id", string="Services")

    @api.onchange("package_id")
    def _onchange_package_id(self):
        if self.package_id:
            room_data = []
            service_data = []
            for room_line in self.package_id.room_line_ids:
                room_data.append((0, 0, {
                    'room_type_id': room_line.room_type_id.id,
                    'quantity': room_line.quantity
                }))
            for service_line in self.package_id.service_line_ids:
                service_data.append((0, 0, {
                    'service_id': service_line.service_id.id,
                    'description': service_line.description,
                    'price': service_line.price
                }))
            self.room_line_ids = room_data
            self.service_line_ids = service_data

    def action_add_package(self):
        room_data = [(0, 0, {
            'checkin_date': self.checkin_date,
            'checkout_date': self.checkout_date,
            'product_id': self.package_id.product_id.id,
            'product_uom': self.package_id.product_id.uom_id.id,
            'price_unit': self.package_id.product_id.list_price,
            'name': self.package_id.name,
        })]
        service_data = []
        for room_line in self.room_line_ids:
            if len(room_line.room_ids) != room_line.quantity:
                raise UserError(_(f"Quantity of rooms is not matching with the selected rooms for {room_line.room_type_id.display_name} type"))
            for room in room_line.room_ids:
                room_data.append((0, 0, {
                    'checkin_date': self.checkin_date,
                    'checkout_date': self.checkout_date,
                    'product_id': room.product_id.id,
                    'product_uom': room.product_id.uom_id.id,
                    'price_unit': 0,
                    'name': f"{self.package_id.name} - {room.name}",
                }))
        
        for service_line in self.service_line_ids:
            service_data.append((0, 0, {
                'product_id': service_line.service_id.product_id.id,
                'product_uom': service_line.service_id.product_id.uom_id.id,
                'price_unit': 0,
                'name': f"{self.package_id.name} - {service_line.service_id.name}",
            }))
        
        self.folio_id.write({
            'room_line_ids': room_data,
            'service_line_ids': service_data,
        })
        self.folio_id.order_id._compute_amounts()


class AddPackageWizardRoomLine(models.TransientModel):
    _name = "add.package.wizard.room.line"
    _description = "Add Package Wizard Room Line"

    wizard_id = fields.Many2one("add.package.wizard", string="Package")
    room_type_id = fields.Many2one("hotel.room.type", string="Room Type")
    room_ids = fields.Many2many("hotel.room", string="Room")
    quantity = fields.Integer(string="Quantity")

class AddPackageWizardServiceLine(models.TransientModel):
    _name = "add.package.wizard.service.line"
    _description = "Add Package Wizard Service Line"

    wizard_id = fields.Many2one("add.package.wizard", string="Package")
    service_id = fields.Many2one("hotel.services", string="Service")
    description = fields.Text(string="Description")
    price = fields.Float(string="Price")