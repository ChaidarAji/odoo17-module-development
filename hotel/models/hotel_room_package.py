from odoo import models, fields, api


class HotelRoomPackage(models.Model):
    _name = "hotel.room.package"
    _description = "Hotel Room Package"

    name = fields.Char(string="Name")
    room_line_ids = fields.One2many("hotel.room.package.room.line", "room_package_id", string="Rooms Type")
    service_line_ids = fields.One2many("hotel.room.package.service.line", "room_package_id", string="Services")
    description = fields.Text(string="Description")
    room_capacity = fields.Integer(string="Room Capacity")
    price = fields.Float(string="Price")
    product_id = fields.Many2one("product.product", "Product", ondelete="cascade")


    def create(self, vals):
        product = self.env["product.product"].create({"name": vals.get("name"),
                                                      'type': 'consu',
                                                      'list_price': vals.get('price')})
        vals.update({"product_id": product.id})
        return super().create(vals)
    
    def write(self, vals):
        if "price" in vals:
            self.product_id.write({"list_price": vals.get("price")})
        return super().write(vals)

class HotelRoomPackageRoomLine(models.Model):
    _name = "hotel.room.package.room.line"
    _description = "Hotel Room Package Room Line"

    room_package_id = fields.Many2one("hotel.room.package", string="Room Package")
    room_type_id = fields.Many2one("hotel.room.type", string="Room Type")
    quantity = fields.Integer(string="Room Quantity")


class HotelRoomPackageServiceLine(models.Model):
    _name = "hotel.room.package.service.line"
    _description = "Hotel Room Package Service Line"

    room_package_id = fields.Many2one("hotel.room.package", string="Room Package")
    service_id = fields.Many2one("hotel.services", string="Service")
    description = fields.Text(string="Description")
    price = fields.Float(string="Price")

    @api.onchange("service_id")
    def _onchange_service_id(self):
        self.description = self.service_id.description
        self.price = self.service_id.list_price
