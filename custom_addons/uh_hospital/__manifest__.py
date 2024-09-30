{
    "name" : "Hospital Management System",
    "author" : "Umme Hani",
    'description': """
        Module for managing hospital patients and records.
    """,
    "License" :"LGPL-3",
    'version' :"17.0.1.1",
    'category': 'Healthcare',
    'depends': ['base','web', 'mail'],
    'demo': [
        'demo/demo.xml',
    ],
    'data': ['security/ir.model.access.csv',  # Access control file
             'views/patients_views.xml',
             'views/patients_readonly_views.xml',
             'views/menu.xml',


    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [

               ],
},

}