from odoo import api, models
from odoo import http, _, exceptions
from odoo.http import request
import base64
class SaleService(models.Model):
    _name = 'service.sale'
    _description = 'Sale Service'
    def getUid(self, kw):
        uid = kw.get('uid')
        if uid:
            uid = int(kw.get('uid'))
        else:
            uid = 1
        return uid
    @api.model
    def get_all(self, kw):
        authorization_header = self.getUid(kw)
        Sale = http.request.env['new.sale'].sudo()
        sales = Sale.search([
            ('user_id', '=', int(authorization_header))
        ])
        if len(sales) == 0:
            raise exceptions.AccessError(message=f"Data Kosong {authorization_header}")
        sale_data = []
        for sale in sales:
            sale_data.append({
                'id': sale.id,
                'date': sale.date,
                'total': sale.total,
                'line_ids': [
                    {
                        'product_id': line.product_id.id, 
                        'name': line.product_id.name, 
                        'price': line.product_id.price, 
                        'qty': line.qty, 
                        'total': line.total,
                        'image': line.product_id.image.decode('ascii') if line.product_id.image else False
                    } for line in sale.line_ids
                ],
            })
        return sale_data
    
    @api.model
    def get_by_id(self, id):
        sale = request.env['new.sale'].sudo().browse(id)
        if sale:
            sale_data = {
                'id': sale.id,
                'date': sale.date,
                'total': sale.total,
                'line_ids': [
                    {
                        'product_id': line.product_id.id, 
                        'name': line.product_id.name, 
                        'price': line.product_id.price, 
                        'qty': line.qty, 
                        'total': line.total,
                        'image': line.product_id.image.decode('ascii') if line.product_id.image else False
                    } for line in sale.line_ids
                ],
            }
            return sale_data
        raise exceptions.UserError(message="Penjualan tidak ditemukan")
    
    