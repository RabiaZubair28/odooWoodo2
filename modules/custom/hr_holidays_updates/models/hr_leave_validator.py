from odoo import models, fields, api


class HrHolidaysValidators(models.Model):
    _inherit = 'hr.holidays.validators'
    _order = 'sequence asc'

    sequence = fields.Integer(
        string="Sequence",
        default=1,
        help="Approval order"
    )

    sequence_type = fields.Selection(
        [
            ('sequential', 'Sequential'),
            ('parallel', 'Parallel'),
        ],
        string="Sequence Type",
        default='sequential',
        required=True,
        help="Defines whether approval is sequential or parallel"
    )

    action_type = fields.Selection(
        [
            ('approve', 'Approve'),
            ('comment', 'Comment Only'),
        ],
        string="Action Type",
        default='approve',
        required=True
    )


    @api.model
    def create(self, vals):
        """
        Rules:
        - Sequence resets per leave type
        - Sequential -> next sequence
        - Parallel -> reuse latest sequence
        """

        leave_type_id = vals.get('holiday_status_id')
        seq_type = vals.get('sequence_type', 'sequential')

        if leave_type_id and not vals.get('sequence'):
            domain = [('holiday_status_id', '=', leave_type_id)]

            last_validator = self.search(
                domain,
                order='sequence desc',
                limit=1
            )

            if not last_validator:
                # First validator for this leave type
                vals['sequence'] = 1

            else:
                if seq_type == 'parallel':
                    # SAME sequence as last step
                    vals['sequence'] = last_validator.sequence
                else:
                    # Sequential → next step
                    vals['sequence'] = last_validator.sequence + 1

        return super().create(vals)