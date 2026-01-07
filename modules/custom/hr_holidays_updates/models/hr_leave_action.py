from odoo import models


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    def action_approve(self):
        res = super().action_approve()

        for leave in self:
            leave.current_sequence += 1

        return res

    def action_refuse(self):
        return super().action_refuse()
   
    def action_open_management_leaves(self):
        action = self.env.ref('hr_holidays.hr_leave_action_manage').read()[0]
        action['context'] = dict(self.env.context, enforce_sequence_visibility=True)
        return action