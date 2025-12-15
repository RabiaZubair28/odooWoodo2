from odoo import models, fields

class HrLeaveHierarchy(models.Model):
    _name = "hr.leave.hierarchy"
    _description = "Leave Approval Hierarchy"

    name = fields.Char(required=True)
    leave_type_id = fields.Many2one('hr.leave.type', required=True)
    step_ids = fields.One2many("hr.leave.hierarchy.step", "hierarchy_id", string="Steps")


class HrLeaveHierarchyStep(models.Model):
    _name = "hr.leave.hierarchy.step"
    _description = "Hierarchy Step"
    _order = "sequence asc"

    hierarchy_id = fields.Many2one("hr.leave.hierarchy", required=True, ondelete="cascade")

    sequence = fields.Integer(required=True)

    approver_ids = fields.Many2many("hr.holidays.validators", string="Approvers")

    mode = fields.Selection([
        ('sequential', "Sequential"),
        ('parallel', "Parallel")
    ], default="sequential", required=True)

    action_type = fields.Selection([
        ('approve', "Approval Required"),
        ('comment', "Comment Only")
    ], default="approve", required=True)

    notify_next = fields.Boolean("Go to Next Step Automatically?", default=True)
