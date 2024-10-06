from odoo import models, fields, api

class HospitalSpeciality(models.Model):
    _name = 'hospital.speciality'
    _description = 'Doctor Speciality'

    name = fields.Char(string='Speciality Name', required=True)
    description = fields.Text(string='Description')
    department_id = fields.Many2one('hospital.department', string='Department', required=True)
    doctor_ids = fields.Many2many('hospital.doctor', string='Doctors')
    doctor_count = fields.Integer(string='Doctor Count', compute='_compute_doctor_count', store=True)
    nurse_ids = fields.Many2many('hospital.nurse', string='Nurses')
    nurse_count = fields.Integer(string='Nurse Count', compute='_compute_nurse_count', store=True)


    @api.depends('doctor_ids')
    def _compute_doctor_count(self):
        """Compute the number of doctors in a speciality."""
        for speciality in self:
            speciality.doctor_count = len(speciality.doctor_ids)

    @api.depends('nurse_ids')
    def _compute_nurse_count(self):
        """Compute the number of nurses in a speciality."""
        for speciality in self:
            speciality.nurse_count = len(speciality.nurse_ids)

    @api.model
    def create(self, vals):
        """Ensure department speciality list updates when a new speciality is created."""
        speciality = super(HospitalSpeciality, self).create(vals)
        if speciality.department_id:
            speciality.department_id.sudo().write({'speciality_ids': [(4, speciality.id)]})
        return speciality

    def write(self, vals):
        """Ensure department speciality list updates when a speciality's department is changed."""
        old_departments = {rec.id: rec.department_id for rec in self}
        res = super(HospitalSpeciality, self).write(vals)
        for speciality in self:
            new_department = speciality.department_id
            old_department = old_departments[speciality.id]

            if old_department != new_department:
                if old_department:
                    old_department.sudo().write({'speciality_ids': [(3, speciality.id)]})
                if new_department:
                    new_department.sudo().write({'speciality_ids': [(4, speciality.id)]})
        return res