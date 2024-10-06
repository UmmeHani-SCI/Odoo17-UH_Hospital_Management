from odoo import models, fields, api

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor Information'
    _inherit = ['mail.thread']

    name = fields.Char(string='Doctor Name', required=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender', required=True, tracking=True)
    dob = fields.Date(string='Date of Birth', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    phone = fields.Char(string='Phone Number', required=True, tracking=True)
    email = fields.Char(string='Email', tracking=True)
    address = fields.Text(string='Address', tracking=True)
    speciality_ids = fields.Many2many('hospital.speciality', string='Specialties', required=True)
    department_id = fields.Many2one('hospital.department', string='Department', compute='_compute_department', store=True, readonly=True)

    @api.depends('speciality_ids')
    def _compute_department(self):
        """Automatically assign department based on the selected specialties."""
        for doctor in self:
            if doctor.speciality_ids:
                # Get the department of the first selected specialty (assuming all specialties belong to the same department)
                doctor.department_id = doctor.speciality_ids[0].department_id
            else:
                doctor.department_id = False

    @api.depends('dob')
    def _compute_age(self):
        """Compute the doctor's age based on date of birth."""
        for record in self:
            if record.dob:
                today = fields.Date.today()
                record.age = today.year - record.dob.year - ((today.month, today.day) < (record.dob.month, record.dob.day))
            else:
                record.age = 0


class HospitalSpeciality(models.Model):
    _name = 'hospital.speciality'
    _description = 'Doctor Speciality'

    name = fields.Char(string='Speciality Name', required=True)
    description = fields.Text(string='Description')
    department_id = fields.Many2one('hospital.department', string='Department', required=True)
    doctor_ids = fields.Many2many('hospital.doctor', string='Doctors')
    doctor_count = fields.Integer(string='Doctor Count', compute='_compute_doctor_count', store=True)

    @api.depends('doctor_ids')
    def _compute_doctor_count(self):
        """Compute the number of doctors in a specialty."""
        for speciality in self:
            speciality.doctor_count = len(speciality.doctor_ids)

    @api.model
    def create(self, vals):
        """Ensure department speciality list updates when a new speciality is created."""
        speciality = super(HospitalSpeciality, self).create(vals)
        if speciality.department_id:
            speciality.department_id.sudo().write({'speciality_ids': [(4, speciality.id)]})
        return speciality

    def write(self, vals):
        """Ensure department speciality list updates when a speciality's department is changed."""
        for speciality in self:
            old_department = speciality.department_id
            res = super(HospitalSpeciality, self).write(vals)
            # If the department is changed, update the department's speciality list
            if 'department_id' in vals:
                new_department = self.env['hospital.department'].browse(vals['department_id'])
                # Remove speciality from the old department
                if old_department:
                    old_department.sudo().write({'speciality_ids': [(3, speciality.id)]})
                # Add speciality to the new department
                if new_department:
                    new_department.sudo().write({'speciality_ids': [(4, speciality.id)]})
        return res


class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'

    name = fields.Char(string='Department Name', required=True)
    description = fields.Text(string='Description')
    speciality_ids = fields.One2many('hospital.speciality', 'department_id', string='Specialties', readonly=True)
    doctor_count = fields.Integer(string='Doctor Count', compute='_compute_doctor_count', store=True)

    @api.depends('speciality_ids.doctor_ids')
    def _compute_doctor_count(self):
        """Compute the number of doctors in a department based on linked specialties."""
        for department in self:
            doctor_ids = department.speciality_ids.mapped('doctor_ids')
            department.doctor_count = len(doctor_ids)

    def write(self, vals):
        """Override the write method to ensure department's speciality list stays in sync."""
        res = super(HospitalDepartment, self).write(vals)
        # No need for additional logic, since specialties auto-link to departments
        return res
