from odoo import models, fields

class HrLeaveApprovalLog(models.Model):
    _name = "hr.leave.approval.log"
    _description = "Leave Approval Log"

    leave_id = fields.Many2one("hr.leave", required=True, ondelete="cascade")
    step_id = fields.Many2one("hr.leave.hierarchy.step", required=True)
    user_id = fields.Many2one("res.users", required=True)

    comment = fields.Text()
    date = fields.Datetime(default=lambda self: fields.Datetime.now())
