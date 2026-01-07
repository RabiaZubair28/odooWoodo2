from odoo import models, fields


class HrLeaveApprovalStatus(models.Model):
    _name = "hr.leave.approval.status"
    _description = "Leave Approval Status"
    _order = "sequence, id"
    leave_id = fields.Many2one(
        "hr.leave",
        required=True,
        ondelete="cascade",
    )

    flow_id = fields.Many2one(
        "hr.leave.approval.flow",
        required=True,
        ondelete="cascade",
    )

    user_id = fields.Many2one(
        "res.users",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        default=10,
        help="Approval order inside a flow (used for sequential mode).",
    )
    approved = fields.Boolean(default=False)
    approved_on = fields.Datetime()