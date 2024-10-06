from odoo import models, fields, api

class HospitalNurse(models.Model):
    _name = 'hospital.nurse'
    _description = 'Nurse Information'
    _inherit = ['mail.thread']

    name = fields.Char(string='Nurse Name', required=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender', required=True, tracking=True)
    dob = fields.Date(string='Date of Birth', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True, tracking=True)
    phone = fields.Char(string='Phone Number', required=True, tracking=True)
    email = fields.Char(string='Email', tracking=True)
    address = fields.Text(string='Address', tracking=True)
    speciality_ids = fields.Many2many('hospital.speciality', string='Specialties', required=True, tracking=True)
    department_id = fields.Many2one('hospital.department', string='Department', compute='_compute_department', store=True, readonly=True, tracking=True)

    @api.depends('speciality_ids')
    def _compute_department(self):
        """Automatically assign department based on the selected specialties."""
        for nurse in self:
            if nurse.speciality_ids:
                nurse.department_id = nurse.speciality_ids[0].department_id
            else:
                nurse.department_id = False

    @api.depends('dob')
    def _compute_age(self):
        """Compute the nurse's age based on date of birth."""
        for record in self:
            if record.dob:
                today = fields.Date.today()
                record.age = today.year - record.dob.year - ((today.month, today.day) < (record.dob.month, record.dob.day))
            else:
                record.age = 0
