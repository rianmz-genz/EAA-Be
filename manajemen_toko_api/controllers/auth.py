from odoo import http, _, exceptions
from odoo.http import request
import json
from datetime import datetime

class AuthController(http.Controller):
    def __init__(self):
        super(AuthController, self).__init__()
        self.helper = request.env['service.helper']
        self.auth_service = request.env['service.auth']
        
    @http.route('/api/login', auth='public', methods=["POST"], csrf=False, cors="*", website=False)
    def login(self, **kw):
        kolom_dibutuhkan = ['email', 'password', 'db']
        try:
            self.helper.validasi_kolom(kw, kolom_dibutuhkan)
        except exceptions.ValidationError as e:
            return self.helper.res_json([], False, f'Err {e}')
        try:
            res = self.auth_service.prosesLogin(kw)
        except exceptions.AccessDenied as e:
            return self.helper.res_json([], False, f'Err {e}')
        return self.helper.res_json(res, True, 'Berhasil login')