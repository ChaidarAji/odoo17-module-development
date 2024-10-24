# -*- coding: utf-8 -*-
# from odoo import http


# class CustomExcelImportData(http.Controller):
#     @http.route('/custom_excel_import_data/custom_excel_import_data', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_excel_import_data/custom_excel_import_data/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_excel_import_data.listing', {
#             'root': '/custom_excel_import_data/custom_excel_import_data',
#             'objects': http.request.env['custom_excel_import_data.custom_excel_import_data'].search([]),
#         })

#     @http.route('/custom_excel_import_data/custom_excel_import_data/objects/<model("custom_excel_import_data.custom_excel_import_data"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_excel_import_data.object', {
#             'object': obj
#         })

