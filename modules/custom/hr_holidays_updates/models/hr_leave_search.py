from odoo import models, api
from odoo.osv import expression


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.model
    def search(self, domain=None, offset=0, limit=None, order=None):
        domain = domain or []

        # Superuser / HR Manager sees everything
        if self.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
            return super().search(domain, offset, limit, order)

        Validator = self.env['hr.holidays.validators']

        validators = Validator.search([
            ('validator_id.user_id', '=', self.env.user.id),
        ])

        allowed_leave_type_ids = validators.mapped('leave_type_id').ids
        allowed_sequences = validators.mapped('sequence')

        visibility_domain = [
            ('holiday_status_id', 'in', allowed_leave_type_ids),
            ('current_sequence', 'in', allowed_sequences),
        ]

        domain = expression.AND([domain, visibility_domain])

        return super().search(domain, offset, limit, order)
