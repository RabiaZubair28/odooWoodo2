from odoo import models, fields
from odoo.exceptions import UserError


class LeaveCommentWizard(models.TransientModel):
    _name = 'leave.comment.wizard'

    comment = fields.Text(required=True)

    def action_submit(self):
        leave = self.env['hr.leave'].browse(self.env.context['active_id'])
        status = leave._get_current_approvers().filtered(
            lambda s: s.user_id == self.env.user
        )

        if not status:
            raise UserError('You are not allowed to act now.')

        status.write({
            'comment': self.comment,
            'state': 'done'
        })

        pending = leave.approval_status_ids.filtered(
            lambda s: s.sequence == leave.current_sequence and s.state == 'pending'
        )

        if not pending:
            sequences = leave.approval_status_ids.filtered(
                lambda s: s.sequence > leave.current_sequence
            ).mapped('sequence')
            if sequences:
                leave.current_sequence = min(sequences)
            else:
                leave.action_approve()

        return {'type': 'ir.actions.act_window_close'}
