{
    'name': 'Custom Excel Import Data',
    'version': '1.0',  # Update this line
    'sequence': 1,
    'category': '',
    'summary': 'Module to Import Excel Data and Create Records for Models',
    'description': """
        
    """,
    'author': 'Doodex',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_excel_import_data_views.xml',
        'views/custom_excel_update_data_views.xml',
        'wizard/wizard_create_record_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
        ],
    },
    'installable': True,
    'application': True,
}


