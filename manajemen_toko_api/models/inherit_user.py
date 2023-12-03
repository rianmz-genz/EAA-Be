# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InheritUser(models.Model):
    _inherit = 'res.user'

    is_active = fields.Boolean()
    
    @api.model
    def activate_user(self):
        self.is_active = True

