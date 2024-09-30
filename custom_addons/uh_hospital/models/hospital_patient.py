
from odoo import api, fields, models
from datetime import date

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Master'
    _inherit =  'mail.thread'

    name = fields.Char(string='Name', required=True, tracking=True)
    dob = fields.Date(string='Date of Birth', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True, tracking=True)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender', required=True , tracking=True)
    date_of_admitted_to_hospital = fields.Date(string='Date of Admitted To Hospital / Checkup', tracking=True)
    phone = fields.Char(string='Phone Number',  tracking=True)
    email = fields.Char(string='Email' , tracking=True)
    address = fields.Text(string='Address' , tracking=True)

    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:
                today = date.today()
                dob = fields.Date.from_string(record.dob)
                record.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            else:
                record.age = 0
