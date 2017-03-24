# -*- coding: utf-8 -*-
{
    'name': "qg_albert",

    'summary': """
        A simple migration script (Migrates PO and SO transaction data from Odoo v8 to v10""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Felix Otoo <ofelix03@gmail.com",
    'website': "http://quantumgroupgh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}