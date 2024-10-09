
from odoo import api, fields, models



class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit =  ['mail.thread']
    _rec_names_search = ['reference','patient_id']
    _rec_name = 'patient_id'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor' , tracking=True)
    patient_id= fields.Many2one('hospital.patient', string='Patient', tracking=True)
    date_appointment = fields.Date(string='Date of Appointment' , tracking=True)
    note = fields.Text(string='Note' , tracking=True)
    reference = fields.Char(string='Reference', default='New', tracking=True)
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('ongoing', 'Ongoing'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
        ],
        string='State',
        default='draft'
        , tracking=True
    )
    appointment_line_ids = (fields.One2many
                            ('hospital.appointment_line', 'appointment_id', string='Lines' )
                           )
    total_qty = fields.Float(compute='_compute_total_qty', store=True ,string='Total Quantity', tracking=True)
    dob = fields.Date(string='Date of Birth', tracking=True, related='patient_id.dob')
    @api.model_create_multi
    def create(self, vals_list):
        print("uh_hospital", vals_list)
        for vals in vals_list:
            if 'reference' not in vals or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or 'New'
        return super(HospitalAppointment, self).create(vals_list)

    @api.depends('appointment_line_ids','appointment_line_ids.qty')
    def _compute_total_qty(self):
        for rec in self:
            total_qty=0
            print(rec.appointment_line_ids)
            for line in rec.appointment_line_ids:
                print('Line Value', line.qty)
                total_qty += line.qty
            rec.total_qty= total_qty

    def action_confirm(self):
        for rec in self:
            rec.state='confirmed'

    def action_ongoing(self):
        for rec in self:
            rec.state='ongoing'

    def action_done(self):
        for rec in self:
            rec.state='done'

    def action_cancel(self):
        for rec in self:
            rec.state='cancel'

    def _compute_display_name(self):
        for rec in self:
            print("values is,"f"[{rec.reference}]{rec.patient_id.name}")
            rec.display_name=f"[{rec.reference}]{rec.patient_id.name}"


class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment_line'
    _description = 'Hospital Appointment Line'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', tracking=True)
    product_id = fields.Many2one(
        'product.product', string='Product', tracking=True , required=True)
    qty = fields.Float(string='Quantity', tracking=True)

    def _valid_field_parameter(self, field, name):
        if name in ('optional', 'tracking'):
            return True
        return super(HospitalAppointmentLine, self)._valid_field_parameter(field, name)