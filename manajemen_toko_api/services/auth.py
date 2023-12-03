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
    
    @api.model
    def processRegister(self, kw):
        name = kw.get('name')
        email = kw.get('email')
        password = kw.get('password')
        image_1920 = kw.get('image_1920')
        image_binary = base64.b64encode(image_1920.read()) if image_1920 else False
        # Buat data baru untuk user
        User = request.env['res.users'].sudo()
        user = User.create({
            'name': name,
            'login': email,
            'email': email,
            'password': password,
            'image_1920': image_binary
        })
        image_base64 = image_binary.decode('utf-8') if image_binary else None
        return {
                    'user_id': user.id,
                    'name': name,
                    'login': email,
                    'email': email,
                    'password': password,
                    'image': image_base64
                }

    @api.model
    def uploadPayment(self, kw):
        Payment = request.env['new.payment'].sudo()
        summary = kw.get('summary')
        user_id = kw.get('user_id')
        image = kw.get('image')
        image_binary = base64.b64encode(image.read()) if image else False
        payment = Payment.create({
            'image': image_binary,
            'summary': summary,
            'user_id': user_id,
        })
        if not payment:
            raise  exceptions.AccessDenied(message="Error create payment")
        image_base64 = image_binary.decode('utf-8') if image_binary else None
        return  {
            'id': payment.id,
            'user_id': user_id,
            'image': image_base64,
            'summary': summary
        }

