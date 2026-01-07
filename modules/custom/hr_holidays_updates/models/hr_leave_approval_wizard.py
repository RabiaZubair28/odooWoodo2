from odoo import models, fields
from odoo.exceptions import UserError


class HrLeaveApprovalWizard(models.TransientModel):
    _name = "hr.leave.approval.wizard"
    _description = "Leave Approval Wizard"

    leave_id = fields.Many2one("hr.leave", required=True, ondelete="cascade")
    comment = fields.Text(string="Comment")

    def action_confirm(self):
        self.ensure_one()
        leave = self.leave_id.exists()
        if not leave:
            return {"type": "ir.actions.act_window_close"}

        if leave.state != "confirm" or not leave.is_pending_for_user(self.env.user):
            raise UserError("You are not authorized to approve this request at this stage.")

        leave.action_approve_by_user(comment=(self.comment or "").strip() or None)
        return {"type": "ir.actions.act_window_close"}