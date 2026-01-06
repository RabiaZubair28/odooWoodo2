{
    'name': 'HRMIS Leave Multi-Level Validation',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Sequential & Parallel Leave Approval',
    'depends': ['hr_holidays'], 
    'data': [
        'security/ir.model.access.csv',
        'views/hr_leave_type_views.xml',
        # 'views/hr_leave_views.xml',
        # 'views/hr_leave_approval_status_views.xml',
        # 'wizard/leave_comment_wizard_view.xml',
    ],
    'installable': True,
    'application': False,
}
