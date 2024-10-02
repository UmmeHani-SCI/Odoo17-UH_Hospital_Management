
from datetime import date
from odoo.exceptions import ValidationError
from odoo import api, fields, models



class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Master'
    _inherit =  'mail.thread'

    name = fields.Char(string='Name', required=True, tracking=True, ondelete='cascade')
    dob = fields.Date(string='Date of Birth', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True, tracking=True)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender', required=True , tracking=True)
    date_of_admitted_to_hospital = fields.Date(string='Date of Admitted To Hospital / Checkup',
                                               tracking=True, optional='show')
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


    def unlink(self):
        for rec in self:
            domain = [('patient_id', '=', rec.id)]  # Correct the syntax here
            appointment = self.env['hospital.appointment'].search(domain)
            if appointment:
                raise ValidationError("You cannot delete the patient now."
                                      "\nAppointments existing for this patient : %s" % rec.name)

        return super(HospitalPatient, self).unlink()  # Ensure proper inheritance call
