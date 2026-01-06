from odoo import models, fields

class HrLeaveApprovalStatus(models.Model):
    _name = 'hr.leave.approval.status'
    _description = 'Leave Approval Status'
    _order = 'sequence'

    leave_id = fields.Many2one('hr.leave', ondelete='cascade')
    user_id = fields.Many2one('res.users', required=True)
    approval_sequence = fields.Integer(default=1)
    action_type = fields.Selection(
        [('comment', 'Comment'), ('approve', 'Approve')]
    )
    state = fields.Selection(
        [('pending', 'Pending'), ('done', 'Done')],
        default='pending'
    )
    comment = fields.Text()
