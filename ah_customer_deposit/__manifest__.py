{
    "name" : "AH Customer Deposit",
    "version" : "17.0.1.0",
    "category" : "Point of Sale",
    "depends" : ['base','sale','point_of_sale'],
    
    "author": "AH",
    'summary': 'POS Customer Deposit',
    "description": """
        Purpose : Customer Deposit
        Features: 
         - Support Sale
         - Support Point of Sale
    """,
    "website" : "",
    'email': "chaidaraji@gmail.com",
    'price': 0,
    'currency': 'USD',
    'images': ['static/description/icon.png'],
    # 'images': ['static/description/main_background.png'],
    "data": [
        'security/ir.model.access.csv',
        'data/customer_deposit_sequence.xml',
        'wizards/account_payment_register_view.xml',
        'views/customer_deposit_menu.xml',
        'views/customer_deposit_view.xml',
        'views/res_partner_view.xml',
        'views/account_journal_view.xml',
        'views/res_config_settings_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'ah_customer_deposit/static/src/js/Screens/PaymentScreen/PaymentScreen.js',
            'ah_customer_deposit/static/src/js/Screens/ProductScreen/ControlButtons/DepositTopupButton.js',
            'ah_customer_deposit/static/src/js/Screens/ReceiptScreen/OrderReceipt.js',
            'ah_customer_deposit/static/src/js/Screens/ReceiptScreen/ReceiptScreen.js',
            'ah_customer_deposit/static/src/js/Screens/DepositPaymentPopUp.js',
            'ah_customer_deposit/static/src/js/models.js',
            'ah_customer_deposit/static/src/js/payment_deposit.js',
            # 'ah_customer_deposit/static/src/js/**/*.js',
            'ah_customer_deposit/static/src/xml/Screens/PartnerListScreen/PartnerLine.xml',
            'ah_customer_deposit/static/src/xml/Screens/PaymentScreen/PaymentScreen.xml',
            'ah_customer_deposit/static/src/xml/Screens/PartnerListScreen/PartnerListScreen.xml',
            'ah_customer_deposit/static/src/xml/Screens/ProductScreen/ControlButtons/DepositTopupButton.xml',
            'ah_customer_deposit/static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml',
            'ah_customer_deposit/static/src/xml/Screens/PaymentScreenPaymentLines.xml',
            'ah_customer_deposit/static/src/xml/Screens/DepositPopUp.xml',
            # 'ah_customer_deposit/static/src/xml/**/*.xml',
        ],
    },
    "auto_install": False,
    "installable": True,
    "application": True,
    'license': 'LGPL-3',
}