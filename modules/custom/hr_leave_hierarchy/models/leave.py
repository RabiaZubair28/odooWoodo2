from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrLeave(models.Model):
    _inherit = "hr.leave"

    hierarchy_id = fields.Many2one(
        "hr.leave.hierarchy",
        readonly=True
    )

    approval_log_ids = fields.One2many(
        "hr.leave.approval.log",
        "leave_id",
        string="Approval History",
        readonly=True
    )

    current_step_id = fields.Many2one(
        "hr.leave.hierarchy.step",
        readonly=True
    )

    approver_ids = fields.Many2many(
    'hr.employee',
    string='Current Approvers'
)


    is_current_approver = fields.Boolean(
        compute="_compute_is_current_approver"
    )

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        leaves = super().create(vals_list)

        for leave in leaves:
            hierarchy = leave.holiday_status_id.hierarchy_id
            if not hierarchy:
                continue

            steps = hierarchy.step_ids.sorted('sequence')
            if not steps:
                continue

            first_step = steps[0]

            leave.write({
                'current_step_id': first_step.id,
                'is_current_approver': True,
                'approver_ids': [(6, 0, first_step.approver_ids.ids)],
            })

            self.env['hr.leave.approval.log'].create({
                'leave_id': leave.id,
                'step_id': first_step.id,
                'action_type': 'forward',
            })

        return leaves

    # ---------------------------------------------------------
    # COMPUTE
    # ---------------------------------------------------------
    def _compute_is_current_approver(self):
        employee = self.env["hr.employee"].search(
            [("user_id", "=", self.env.user.id)],
            limit=1
        )

        for leave in self:
            leave.is_current_approver = bool(
                employee
                and leave.current_step_id
                and employee in leave.current_step_id.approver_ids
            )

    # ---------------------------------------------------------
    # APPROVAL OVERRIDE
    # ---------------------------------------------------------
    def action_approve(self):
        for leave in self:
            if leave.hierarchy_id and leave.current_step_id:
                leave._process_hierarchy_step()
            else:
                super(HrLeave, leave).action_approve()

    # ---------------------------------------------------------
    # CORE WORKFLOW
    # ---------------------------------------------------------
    def _process_hierarchy_step(self):
        self.ensure_one()

        step = self.current_step_id

        employee = self.env["hr.employee"].search(
            [("user_id", "=", self.env.user.id)],
            limit=1
        )

        if employee not in step.approver_ids:
            raise ValidationError("You are not an approver for this step.")

        # Log action
        self.env["hr.leave.approval.log"].create({
            "leave_id": self.id,
            "step_id": step.id,
            "user_id": self.env.user.id,
            "action_type": step.action_type,
        })

        # COMMENT ONLY → no forwarding
        if step.action_type == "comment":
            return

        # PARALLEL MODE → wait for all
        if step.mode == "parallel":
            logs = self.env["hr.leave.approval.log"].search([
                ("leave_id", "=", self.id),
                ("step_id", "=", step.id),
                ("action_type", "=", "approve"),
            ])
            if len(logs) < len(step.approver_ids):
                return

        # MOVE TO NEXT STEP
        steps = self.hierarchy_id.step_ids.sorted("sequence")
        idx = steps.ids.index(step.id)

        if idx + 1 < len(steps):
            self.current_step_id = steps[idx + 1]

            if step.notify_next:
                self.message_post(
                    body="Leave forwarded to next approval step."
                )
        else:
            super().action_approve()
