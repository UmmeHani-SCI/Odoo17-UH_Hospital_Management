from odoo import models, fields

class DoctorSpecialties(models.Model):
    _name = 'hospital.doctor_specialties'
    _description = 'Doctor Specialties'

    name = fields.Char(string='Specialty', required=True)
