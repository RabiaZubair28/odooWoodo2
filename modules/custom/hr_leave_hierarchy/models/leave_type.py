from odoo import models, fields

class HrLeaveType(models.Model):
    _inherit = "hr.leave.type"

    hierarchy_id = fields.Many2one(
        "hr.leave.hierarchy",
        string="Approval Hierarchy"
    )
