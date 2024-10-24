from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import openpyxl
import base64
import re
from io import BytesIO

class WizardCreateRecord(models.TransientModel):
    _name = 'wizard.create.record'

    import_data_id = fields.Many2one("custom.excel.import.data", string="Excel Data Import")
    model_id = fields.Many2one("ir.model", string="Records Model to Create")
    prevent_duplicate = fields.Boolean(string="Prevent Duplication", default=True)
    prevent_duplicate_existing = fields.Boolean(string="Prevent Duplication with Existing", default=True)
    line_ids = fields.One2many("wizard.create.record.line", "wizard_id", string="Lines")
    skip_uncomplete = fields.Boolean(string="Skip Uncomplete Data", default=False)

    def button_create_record(self):
        try:
            wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.import_data_id.file)), read_only=True)
            ws = wb.active
        except:
            raise UserError("Please insert a valid file")
        datas = []
        req_fields = self.line_ids.mapped('field_id').filtered(lambda x: x.required)
        for record in ws.iter_rows(min_row=2, max_row=None, min_col=0,max_col=None, values_only=True):
            if all(x is None for x in record):
                continue
            data = {}
            for line in self.line_ids.filtered(lambda x: x.field_id):
                val = record[line.header_data_id.index_no]
                if val and (isinstance(val,str) and not val.strip()):
                    continue
                #Check if the data doest exist in existing record. if exist pass
                if self.prevent_duplicate_existing and line.field_id.name == 'name' and val:
                    exist_val = self.env[self.model_id.model].search([('name', '=', val.strip())])
                    if exist_val:
                        data = False
                        break
                if line.field_id.ttype == 'many2one' and val:
                    valm = self.env[line.field_id.relation].search([('name', '=', re.sub(r'\s+', ' ', val.strip()).strip())])
                    if not valm and not line.force_create:
                        raise UserError(_("Data %s di %s tidak ditemukan")%(val, line.field_id.field_description))
                    elif not valm and line.force_create:
                        valm = self.env[line.field_id.relation].create({'name': val.strip()})
                    data[line.field_id.name] = valm.sorted(key=lambda d: d.id)[line.use_index].id
                elif line.field_id.ttype == 'many2many' and val:
                    valsplit = val.split(",")
                    vdata = []
                    for v in valsplit:
                        vd = self.env[line.field_id.relation].search([('name', '=', v.strip())])
                        if not vd and not line.force_create:
                            raise UserError(_("Data %s di %s tidak ditemukan")%(v, line.field_id.field_description))
                        elif not vd and line.force_create:
                            vd = self.env[line.field_id.relation].create({'name': v.strip()})
                        vdata.append(vd.id)
                    data[line.field_id.name] = [(6,0,vdata)]

                else:
                    if val:
                        data[line.field_id.name] = val if not isinstance(val,str) else val.strip()
            if data:
                if self.prevent_duplicate:
                    if data not in datas and data:
                        datas.append(data)
                    else:
                        continue
                else:
                    datas.append(data)

        for rdata in datas:
            datakey = rdata.keys()
            complete = True
            for reqf in req_fields:
                print('aaaaaaaaaaaaaaaaaaaaaa', reqf.name, reqf.name not in datakey, datakey, req_fields)
                if reqf.name not in datakey and self.skip_uncomplete:
                    print('aaaaaaaaaaaaaaaaaaaaaa1', reqf.name, reqf.name not in datakey, datakey, req_fields)
                    complete = False
                    break
            print('???????????????????????????', rdata, complete)
            if complete:        
                self.env[self.model_id.model].create(rdata)
        return True

class WizardCreateRecord(models.TransientModel):
    _name = 'wizard.create.record.line'

    wizard_id = fields.Many2one("wizard.create.record")
    header_data_id = fields.Many2one('custom.excel.import.data.header', string="Header Name")
    field_id = fields.Many2one("ir.model.fields", string="Fields")
    force_create = fields.Boolean(string="Force Create", default=False)
    use_index = fields.Integer(string="Use Index", default=0)