from odoo import models, fields, api

class Payment(models.Model):
    _name = 'new.payment'
    _description = 'Payment'

    user_id = fields.Many2one('res.users', string="User")
    image = fields.Binary()
    summary = fields.Char()


