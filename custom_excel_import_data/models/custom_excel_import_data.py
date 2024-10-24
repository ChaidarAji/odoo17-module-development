# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import openpyxl
import base64
from io import BytesIO

class CustomExcelImportData(models.Model):
    _name = 'custom.excel.import.data'
    _description = 'custom.excel.import.data'

    name = fields.Char()
    file = fields.Binary(string="File", required=True)
    filename = fields.Char(string="Filename")
    header_line_ids = fields.One2many("custom.excel.import.data.header", "import_data_id", string="Header Data")

    def generate_header(self):
        try:
            wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file)), read_only=True)
            ws = wb.active
        except:
            raise UserError("Please insert a valid file")

        self.header_line_ids.unlink()
        header_data = self.env['custom.excel.import.data.header']
        header = True
        for record in ws.iter_rows(min_row=1, max_row=2, min_col=0,max_col=None, values_only=True):
            if header:
                for index, header_name in enumerate(record):
                    header_data.create({'name': header_name,
                                        'index_no': index,
                                        'import_data_id': self.id})
                header = False
            else:
                for header in self.header_line_ids:
                    header.write({'example': record[header.index_no]})

    def action_create_record(self):
        header_data = []
        for head in self.header_line_ids:
            header = self.env['wizard.create.record.line'].create({'header_data_id': head.id})
            header_data.append(header.id)
        return {
            'name': _('Create Records'),
            'res_model': 'wizard.create.record',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'context': {
                'active_model': 'custom.excel.import.data',
                'default_import_data_id': self.id,
                'default_line_ids': [(6,0,header_data)]
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
            }

class CustomExcelImportDataHeader(models.Model):
    _name = 'custom.excel.import.data.header'

    name = fields.Char(string="Header Name")
    example = fields.Char(string="Example Value")
    index_no = fields.Integer(string="Index No.")
    import_data_id = fields.Many2one("custom.excel.import.data")