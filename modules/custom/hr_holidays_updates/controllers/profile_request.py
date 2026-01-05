from odoo import http
from odoo.http import request


class HRMISProfileRequest(http.Controller):

    @http.route('/hrmis/profile/request', type='http', auth='user', website=True)
    def profile_request_form(self):
        user = request.env.user
        employee = user.employee_id

        if not employee:
            return request.render(
                'hr_holidays_updates.hrmis_error',
                {'error': 'No employee linked to your user.'}
            )

        ProfileRequest = request.env['hrmis.employee.profile.request'].sudo()

        # Get existing draft/submitted request
        req = ProfileRequest.search([
            ('employee_id', '=', employee.id),
            ('state', 'in', ['draft', 'submitted'])
        ], limit=1)

        # If no request exists, create a draft
        if not req:
            req = ProfileRequest.create({
                'employee_id': employee.id,
                'user_id': user.id,
                'state': 'draft',
            })

        # Build pre_fill dictionary: take from employee, override with req if exists
        pre_fill = {
            'hrmis_employee_id': employee.hrmis_employee_id or '',
            'hrmis_cnic': employee.hrmis_cnic or '',
            'hrmis_father_name': employee.hrmis_father_name or '',
            'gender': employee.gender or '',
            'hrmis_joining_date': employee.hrmis_joining_date or '',
            'hrmis_bps': employee.hrmis_bps or '',
            'hrmis_cadre': employee.hrmis_cadre or '',
            'hrmis_designation': employee.hrmis_designation or '',
            'district_id': employee.district_id.id if employee.district_id else False,
            'facility_id': employee.facility_id.id if employee.facility_id else False,
            'hrmis_contact_info': employee.hrmis_contact_info or '',
        }

        # Override with existing draft/submitted request values
        if req:
            for field in pre_fill.keys():
                value = getattr(req, field, None)
                if value:
                    if field in ['district_id', 'facility_id']:
                        pre_fill[field] = value.id
                    else:
                        pre_fill[field] = value

        # Show message if request is already submitted
        submitted_msg = None
        if req.state == 'submitted':
            submitted_msg = "You already have a submitted profile update request. You cannot submit another until it is processed."

        return request.render(
            'hr_holidays_updates.hrmis_profile_request_form',
            {
                'employee': employee,
                'req': req,
                'pre_fill': pre_fill,
                'districts': request.env['hrmis.district.master'].sudo().search([]),
                'facilities': request.env['hrmis.facility.type'].sudo().search([]),
                'active_menu': 'user_profile',
                'current_employee': employee,
                'info': submitted_msg, 
            }
        )


    @http.route(
        '/hrmis/profile/request/submit',
        type='http',
        auth='user',
        website=True,
        methods=['POST'],
        csrf=True
    )
    def submit_profile_request(self, **post):
        user = request.env.user
        employee = user.employee_id
        req = request.env['hrmis.employee.profile.request'].sudo().browse(
            int(post.get('request_id'))
        )

        if not req.exists():
            error = 'Invalid request.'
            return self._render_profile_form(employee, req, error=error)

        # --------------------------
        # VALIDATE REQUIRED FIELDS
        # --------------------------
        required_fields = {
            'hrmis_employee_id': 'Employee ID / Service Number',
            'hrmis_cnic': 'CNIC',
            'hrmis_father_name': "Father's Name",
            'gender': 'Gender',
            'hrmis_joining_date': 'Joining Date',
            'hrmis_bps': 'BPS',
            'hrmis_cadre': 'Cadre',
            'hrmis_designation': 'Designation',
            'district_id': 'District',
            'facility_id': 'Facility',
        }

        missing = []
        for field, label in required_fields.items():
            value = post.get(field)
            if not value:
                missing.append(label)

        if missing:
            error = "Please complete the following fields before submitting:\n• " + "\n• ".join(missing)
            return self._render_profile_form(employee, req, error=error)

        # --------------------------
        # VALIDATE DATE FIELDS
        # --------------------------
        from datetime import datetime, date

        today = date.today()
        joining_date_str = post.get('hrmis_joining_date')
        try:
            joining_date = datetime.strptime(joining_date_str, '%Y-%m-%d').date()
            if joining_date > today:
                error = "Joining Date cannot be in the future."
                return self._render_profile_form(employee, req, error=error)
        except Exception:
            error = "Invalid Joining Date format."
            return self._render_profile_form(employee, req, error=error)

        # birthday validation if needed
        birthday_str = post.get('birthday')
        if birthday_str:
            try:
                birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
                if birthday > today:
                    error = "Date of Birth cannot be in the future."
                    return self._render_profile_form(employee, req, error=error)
            except Exception:
                error = "Invalid Date of Birth format."
                return self._render_profile_form(employee, req, error=error)

        # --------------------------
        # VALIDATE BPS
        # --------------------------
        try:
            bps = int(post.get('hrmis_bps'))
            if bps < 6 or bps > 22:
                error = "BPS must be between 6 and 22."
                return self._render_profile_form(employee, req, error=error)
        except Exception:
            error = "Invalid BPS value."
            return self._render_profile_form(employee, req, error=error)

        # --------------------------
        # VALIDATE UNIQUENESS
        # --------------------------
        HRRequest = request.env['hrmis.employee.profile.request'].sudo()
        cnic = post.get('hrmis_cnic')
        hr_id = post.get('hrmis_employee_id')

        # CNIC unique
        if HRRequest.search_count([('hrmis_cnic', '=', cnic), ('id', '!=', req.id)]):
            error = "CNIC must be unique."
            return self._render_profile_form(employee, req, error=error)

        # Employee ID unique
        if HRRequest.search_count([('hrmis_employee_id', '=', hr_id), ('id', '!=', req.id)]):
            error = "Employee ID / Service Number must be unique."
            return self._render_profile_form(employee, req, error=error)

        # --------------------------
        # WRITE THE RECORD
        # --------------------------
        req.write({
            'hrmis_employee_id': hr_id,
            'hrmis_cnic': cnic,
            'hrmis_father_name': post.get('hrmis_father_name'),
            'gender': post.get('gender'),
            'hrmis_joining_date': joining_date_str,
            'hrmis_bps': bps,
            'hrmis_cadre': post.get('hrmis_cadre'),
            'hrmis_designation': post.get('hrmis_designation'),
            'district_id': int(post.get('district_id')),
            'facility_id': int(post.get('facility_id')),
            'hrmis_contact_info': post.get('hrmis_contact_info'),
            'state': 'submitted',
        })

        success = 'Profile update request submitted successfully.'
        return self._render_profile_form(employee, req, success=success)



    # Helper to render the same form with messages
    def _render_profile_form(self, employee, req, error=None, success=None):
        return request.render(
            'hr_holidays_updates.hrmis_profile_request_form',
            {
                'employee': employee,
                'req': req,
                'districts': request.env['hrmis.district.master'].sudo().search([]),
                'facilities': request.env['hrmis.facility.type'].sudo().search([]),
                'active_menu': 'user_profile',
                'current_employee': employee,
                'error': error,
                'success': success,
            }
        )
