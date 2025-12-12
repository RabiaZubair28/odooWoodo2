from odoo import models, fields, api

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    # Custom field to link HRMIS profile (optional, may not be needed for dynamic filtering)
    hrmis_profile_id = fields.Many2one('hrmis.user.profile', string="HRMIS Profile")

    # Example: override a method (keep original functionality)
    def _check_allocation(self, employee_id, request_date_from, request_date_to):
        res = super()._check_allocation(employee_id, request_date_from, request_date_to)
        # Add your custom validation logic here
        return res
    
    @api.onchange('hrmis_profile_id')
    def _onchange_employee_filter_leave_type(self):
        for rec in self:
            if rec.employee_id and rec.hrmis_profile_id:
                gender = rec.hrmis_profile_id.gender
                if gender == 'male':
                    # hide maternity leave
                    rec.leave_type_id = False
                    return {
                        'domain': {
                            'holiday_status_id': [('name', '!=', 'Maternity Leave')]
                        }
                    }
                else:
                    # no restriction for female
                    return {
                        'domain': {
                            'holiday_status_id': []
                        }
                    }
    
