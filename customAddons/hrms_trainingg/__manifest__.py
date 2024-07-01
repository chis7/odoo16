# -- coding: utf-8 --
{
    'name': "HRMS Employee Training Data",
    'version': '16.0.1.0.0',
    'summary': """Manage training data for the Civil Service""",
    'description': """Manage training data for the Civil Service""",
    'category': 'Generic Modules/Human Resources',
    'author': 'Chisenga Musonda',
    'website': "https://www.moh.gov.zm",
    'depends': [
        'mail',
        'base',
        'hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/trainingPlan.xml',
        'views/typeOfTraining.xml',
        'views/fieldOfStudy.xml',
        'views/levelOfStudy.xml',
    ],
    'demo': [],
    'images': ["static/description/banner.png"],
    'license': "AGPL-3",
    'installable': True,
    'application': False,
}
