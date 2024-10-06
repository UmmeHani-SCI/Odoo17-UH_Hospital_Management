from odoo import models, fields , api

class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'

    name = fields.Char(string='Department Name', required=True)
    description = fields.Text(string='Description')
    speciality_ids = fields.One2many('hospital.speciality', 'department_id', string='Specialities', readonly=True)
    doctor_count = fields.Integer(string='Doctor Count', compute='_compute_doctor_count', store=True)
    nurse_count = fields.Integer(string='Nurse Count', compute='_compute_nurse_count', store=True)

    @api.depends('speciality_ids.doctor_ids')
    def _compute_doctor_count(self):
        """Compute the number of doctors in a department based on its linked specialities."""
        for department in self:
            doctor_ids = department.speciality_ids.mapped('doctor_ids')
            department.doctor_count = len(doctor_ids)

    @api.depends('speciality_ids.nurse_ids')
    def _compute_nurse_count(self):
        """Compute the number of nurses in a department based on linked specialities."""
        for department in self:
            nurse_ids = department.speciality_ids.mapped('nurse_ids')
            department.nurse_count = len(nurse_ids)