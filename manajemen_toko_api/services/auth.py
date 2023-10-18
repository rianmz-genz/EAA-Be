from odoo import api, models
from odoo import http, _, exceptions
from odoo.http import request
class AuthService(models.Model):
    _name = 'service.auth'
    _description = 'Auth Service'

    @api.model
    def prosesLogin(self, kw):
        login = kw.get('email')
        password = kw.get('password')
        db = kw.get('db')
        try:
            http.request.session.authenticate(db, login, password)
        except Exception as e:
            raise exceptions.AccessDenied(message=e)
        return request.env['ir.http'].session_info()