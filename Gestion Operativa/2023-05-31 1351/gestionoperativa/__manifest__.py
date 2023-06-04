# -*- coding: utf-8 -*-
{
    'name': "gestionoperativa",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','vuelo_base','web_google_maps'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/parteaereo.xml',
        'views/partemaritimo.xml',
        'views/parteterrestre.xml',
        'views/configmar.xml',
        'views/tiposituacion.xml',
        'views/configavi.xml',
        'views/configter.xml',
        'views/templates.xml',
        'views/tiporesultado.xml',
        'views/tipooperacion.xml',
        'views/tipoplataforma.xml',
        'views/areasoperacion.xml',
        'views/resultadosobtenidos.xml',
        'data/data_tipo_situacion.xml',
        'data/data_tipooperacion.xml',
        'data/data_estado_situacion_detalle.xml',
        'data/data_cab_parte_aereo.xml',
        'data/data_tipoplataforma.xml',
        
    ],
    'assets': {
        'web.assets_backend': [
            'gestionoperativa/static/src/css/test.css',
        ],
    },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
