# -*- coding: utf-8 -*-

{
    'name': "Default Company in Partner",
    'version': '16.0.1.0',
    'category': 'Partner',
    'summary': 'Set current company as default in partner multi-company field',
    'description': """
        When creating a new partner, automatically set the current company
        in the companies field (partner_multi_company module required)
    """,
    'depends': ['partner_multi_company'],
    'data': [
        'security/ir.model.access.csv',
     
    ],
    'qweb': [],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'author': "Alexander Falcon",
    # 'website': "http://www.yourcompany.com",
    'license': 'LGPL-3',
}
