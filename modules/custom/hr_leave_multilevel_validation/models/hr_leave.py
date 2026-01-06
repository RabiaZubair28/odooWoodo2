from odoo import models, fields
from odoo.exceptions import UserError

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    approval_status_ids = fields.One2many(
        'hr.leave.approval.status',
        'leave_id'
    )

    current_sequence = fields.Integer(default=1)

    def action_submit(self):
        res = super().action_submit()

        for leave in self:
            if leave.holiday_status_id.leave_validation_type != 'multi':
                continue

            validators = leave.holiday_status_id.validator_ids
            if not validators:
                raise UserError('No approval hierarchy defined.')

            leave.approval_status_ids.unlink()

            for v in validators:
                self.env['hr.leave.approval.status'].create({
                    'leave_id': leave.id,
                    'user_id': v.user_id.id,
                    'sequence': v.sequence,
                    'action_type': v.action_type,
                })

            leave.current_sequence = min(validators.mapped('sequence'))

        return res
