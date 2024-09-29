
from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Master'

    name = fields.Char(string='Name', required=True)
    date_of_birth= fields.Date(string='DOB')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")