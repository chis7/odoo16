# -- coding: utf-8 --
{
    'name': "HRMS Employee Training Data",
    'version': '16.0.1.0.0',
    'summary': """Manage training data for the Civil Service""",
    'description': """Manage training data for the Civil Service""",
    'category': 'Generic Modules/Human Resources',
    'author': 'Chisenga Musonda',
    'website': "",
    'depends': [
        'mail',
        'base',
        'hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/createTrainingPlanView.xml',
        'views/trainingPlan.xml',
        'views/trainingPlanApprovalHRDC.xml',
        'views/trainingPlanApprovalPS.xml',
        'views/trainingPlanApprovalPSMD.xml',
        'views/typeOfTraining.xml',
        'views/fieldOfStudy.xml',
        'views/levelOfStudy.xml',
        'views/training_views.xml',
    ],
    'demo': [],
    'images': ["static/description/banner.png"],
    'license': "AGPL-3",
    'installable': True,
    'application': False,
}
