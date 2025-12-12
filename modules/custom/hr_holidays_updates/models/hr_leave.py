from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.onchange('employee_id')
    def _onchange_employee_filter_leave_type(self):
        if not self.employee_id:
            return {'domain': {'holiday_status_id': []}}

        # Get employee HRMIS profile
        profile = self.hrmis_profile_id
        if not profile:
            return

        gender = profile.gender

        # Get leave types
        leave_type_model = self.env['hr.leave.type']
        if gender == 'male':
            maternity = leave_type_model.search([('name', '=', 'Maternity Leave')], limit=1)
            domain = [('id', '!=', maternity.id)] if maternity else []
        elif gender == 'female':
            paternity = leave_type_model.search([('name', '=', 'Paternity Leave')], limit=1)
            domain = [('id', '!=', paternity.id)] if paternity else []
        else:
            domain = []

        return {'domain': {'holiday_status_id': domain}}
