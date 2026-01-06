from odoo import models, fields

class HrLeaveValidator(models.Model):
    _inherit = 'hr.holidays.validators'
    # _description = 'Leave Type Validator'
    # _order = 'sequence'

    leave_type_id = fields.Many2one(
        'hr.leave.type',
        required=True,
        ondelete='cascade'
    )

    user_id = fields.Many2one(
        'res.users',
        required=True
    )

    approval_sequence = fields.Integer(default=1)

    sequence_type = fields.Selection(
        [('sequence', 'Sequential'), ('parallel', 'Parallel')],
        default='sequence',
        required=True
    )

    action_type = fields.Selection(
        [('comment', 'Comment'), ('approve', 'Approve')],
        required=True
    )
