{
    'name': 'HRMIS Employee PDF',
    'version': '1.0',
    'summary': 'Print Employee Profile PDF',
    'depends': ['hr'],
    'data': [
        'reports/hrmis_employee_report.xml',
        'reports/employee_profile_template.xml',
        'views/hr_employee_view.xml',
    ],
    'installable': True,
    'application': False,
}
