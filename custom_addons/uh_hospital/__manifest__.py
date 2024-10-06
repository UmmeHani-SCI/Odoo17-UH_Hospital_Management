{
    'name' : "Hospital Management System",
    "author" : "Umme Hani",
    'description': ' Module for managing hospital patients and records.',
    'license': 'LGPL-3',

    'version' :"17.0.1.1",
    'category': 'Healthcare',
    'depends': ['base','web', 'mail'],

    'data': ['security/ir.model.access.csv',  # Access control file
             'data/sequence.xml',
             'views/patients_views.xml',
             'views/patients_readonly_views.xml',
             'views/appoinment_views.xml',
             'views/appointment_line_views.xml',
             'views/doctor.xml',
             'views/speciality_views.xml',
             'views/department_views.xml',
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
