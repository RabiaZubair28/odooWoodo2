from odoo import models, fields

class HrLeaveApprovalLine(models.Model):
    _name = 'hr.leave.approval.line'
    _description = 'Leave Approval Line'
    
    leave_id = fields.Many2one('hr.leave', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', required=True)
    sequence = fields.Integer(required=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
    ], default='pending')
