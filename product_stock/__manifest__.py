# -*- coding: utf-8 -*-
{
    'name': "Product Stock",

    'summary': """
            Short (1 phrase/line) summary of the module's purpose, used as
            subtitle on modules listing or apps.openerp.com""",

    'description': """
            Long description of module's purpose
        """,
    'category': 'Tools',
    'sequence': 1,
    'version': '14.0',
    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'point_of_sale', 'stock',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/stock_view.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [
        'static/src/xml/stock.xml',

    ],

}
