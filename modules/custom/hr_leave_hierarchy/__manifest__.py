{
    'name': "HR Leave Hierarchy",
    'version': "1.0",
    'author': "Humza Shaikh",
    'category': "Human Resources",
    'summary': "Multi-level custom leave approval workflow",
    'depends': ['hr_holidays', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/actions.xml',
        'views/menu.xml',
        'views/hierarchy_views.xml',
        'views/leave_views.xml',
    ],
    'installable': True,
    'application': True,
}
