# -*- coding: utf-8 -*-
{
    'name': "PRODUCT WARRANTY",
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'category': 'Tools',
    'sequence': 1,
    'version': '13.1',
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'security/sale_security.xml',
        'wizards/warranty_wizards.xml',
        'views/views.xml',
        'views/warranty_locations.xml',
        'views/templates.xml',
        'reports/report.xml',
        'reports/warranty_card.xml',


    ],

    'demo': [
        'demo/demo.xml',
    ],

    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
