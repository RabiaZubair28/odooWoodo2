from odoo import models, api
from odoo.osv import expression


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    # --------------------------------
    # Internal helper
    # --------------------------------
    def _approval_visibility_domain(self):
        if self.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
            return []

        Validator = self.env['hr.holidays.validators']

        validators = Validator.search([
            ('validator_id.user_id', '=', self.env.user.id)
        ])

        if not validators:
            return [('id', '=', -1)]

        return [
            ('holiday_status_id', 'in', validators.mapped('leave_type_id').ids),
            ('current_sequence', 'in', validators.mapped('sequence')),
        ]

    # --------------------------------
    # SEARCH
    # --------------------------------
    @api.model
    def search(self, domain=None, offset=0, limit=None, order=None):
        domain = domain or []
        domain = expression.AND([domain, self._approval_visibility_domain()])
        return super().search(domain, offset, limit, order)

    # --------------------------------
    # SEARCH_READ (used by Management)
    # --------------------------------
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = domain or []
        domain = expression.AND([domain, self._approval_visibility_domain()])
        return super().search_read(domain, fields, offset, limit, order)

    # --------------------------------
    # READ_GROUP (used by kanban / stats)
    # --------------------------------
    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        domain = expression.AND([domain, self._approval_visibility_domain()])
        return super().read_group(domain, fields, groupby, offset, limit, orderby, lazy)

    # --------------------------------
    # NAME_SEARCH (used by M2O lookups)
    # --------------------------------
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        args = expression.AND([args, self._approval_visibility_domain()])
        return super().name_search(name, args, operator, limit)
