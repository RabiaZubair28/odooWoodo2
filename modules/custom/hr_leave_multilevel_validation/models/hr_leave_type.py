from odoo import models, fields

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    leave_validation_type = fields.Selection(
        selection_add=[('multi', 'Multi-Level Approval')]
    )

    validator_ids = fields.One2many(
        'hr.holidays.validators',
        'leave_type_id',
        string='Validators'
    )
