from odoo import models, fields

class HrLeaveHierarchy(models.Model):
    _name = "hr.leave.hierarchy"
    _description = "Leave Approval Hierarchy"

    name = fields.Char(required=True)

    step_ids = fields.One2many(
        "hr.leave.hierarchy.step",
        "hierarchy_id",
        string="Steps"
    )


class HrLeaveHierarchyStep(models.Model):
    _name = "hr.leave.hierarchy.step"
    _description = "Leave Hierarchy Step"
    _order = "sequence"

    hierarchy_id = fields.Many2one(
        "hr.leave.hierarchy",
        required=True,
        ondelete="cascade"
    )

    sequence = fields.Integer(required=True)

    approver_ids = fields.Many2one(
        "hr.employee",
        string="Approvers"
    )

    mode = fields.Selection(
        [
            ("sequential", "Sequential"),
            ("parallel", "Parallel"),
        ],
        default="sequential",
        required=True
    )

    action_type = fields.Selection(
        [
            ("approve", "Approval Required"),
            ("comment", "Comment Only"),
        ],
        default="approve",
        required=True
    )

    notify_next = fields.Boolean(
        string="Notify Next Step Automatically",
        default=True
    )
