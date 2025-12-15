from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrLeave(models.Model):
    _inherit = "hr.leave"

    hierarchy_id = fields.Many2one("hr.leave.hierarchy")
    current_step_id = fields.Many2one("hr.leave.hierarchy.step")

    @api.model_create_multi
    def create(self, vals_list):
        leaves = super().create(vals_list)

        for leave in leaves:
            # attach hierarchy automatically
            hierarchy = leave.env['hr.leave.hierarchy'].search([
                ('leave_type_id', '=', leave.holiday_status_id.id)
            ], limit=1)

            if hierarchy:
                leave.hierarchy_id = hierarchy
                first_step = hierarchy.step_ids.sorted('sequence')[0]
                leave.current_step_id = first_step.id

        return leaves

    def action_process_step(self, comment=""):
        self.ensure_one()
        user = self.env.user
        step = self.current_step_id

        if not step:
            raise ValidationError("No hierarchy step defined.")

        if user not in step.approver_ids:
            raise ValidationError("You are not allowed to act on this step.")

        # Log action
        self.env['hr.leave.approval.log'].create({
            'leave_id': self.id,
            'step_id': step.id,
            'user_id': user.id,
            'comment': comment,
        })

        # PARALLEL MODE → Check if all approvers finished
        if step.mode == "parallel":
            logs = self.env['hr.leave.approval.log'].search([
                ('leave_id', '=', self.id),
                ('step_id', '=', step.id)
            ])
            if len(logs) < len(step.approver_ids):
                return  # still waiting for others

        # Move to next step
        next_step = self.hierarchy_id.step_ids.filtered(
            lambda s: s.sequence == step.sequence + 1
        )

        if next_step:
            self.current_step_id = next_step.id
        else:
            # Final approval
            self.action_validate()
