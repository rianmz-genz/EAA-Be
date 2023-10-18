from odoo import http, _
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception
import json

class SaleApiController(http.Controller):
    def __init__(self):
        super(SaleApiController, self).__init__()
        self.helper = request.env['service.helper']
        self.sale_service = request.env['service.sale']
        
    @http.route('/api/sale/<int:sale_id>', auth='public', methods=['GET'], csrf=False)
    @serialize_exception
    def get_sale(self, sale_id, **kw):
        try:
            sale_data = self.sale_service.get_by_id(sale_id)
        except Exception as e:
            return self.helper.res_json({}, False, f'Err {e}')
        return self.helper.res_json(sale_data, True, 'Berhasil mendapatkan penjualan')
    
    @http.route('/api/sale/get_all', auth='public', methods=['GET'], csrf=False)
    def get_all_sales(self, **kw):
        sale_data = self.sale_service.get_all()
        return self.helper.res_json(sale_data, True, 'Berhasil mendapatkan semua penjualan')

    @http.route('/api/sale/create', auth='public', methods=['POST'], csrf=False)
    @serialize_exception
    def create_sale(self, **kw):
        sale_data = json.loads(request.httprequest.data)
        sale = request.env['new.sale'].sudo().create({
            'date': sale_data.get('date'),
        })
        if 'line_ids' in sale_data:
            for line in sale_data['line_ids']:
                product_id = line.get('product_id')
                qty = line.get('qty')
                if product_id and qty:
                    request.env['new.saleline'].sudo().create({
                        'product_id': product_id,
                        'qty': qty,
                        'sale_id': sale.id,
                    })
        return self.helper.res_json({
                'id': sale.id
            }, True, 'Berhasil membuat penjualan')

    # @http.route('/api/sale/update/<int:sale_id>', auth='public', methods=['PUT'], csrf=False)
    # @serialize_exception
    # def update_sale(self, sale_id, **kw):
    #     sale = request.env['new.sale'].sudo().browse(sale_id)
    #     if sale:
    #         sale_data = json.loads(request.httprequest.data)
    #         sale.write({
    #             'date': sale_data.get('date'),
    #         })
    #         sale.line_ids.unlink()
    #         if 'line_ids' in sale_data:
    #             for line in sale_data['line_ids']:
    #                 product_id = line.get('product_id')
    #                 qty = line.get('qty')
    #                 if product_id and qty:
    #                     request.env['new.saleline'].sudo().create({
    #                         'product_id': product_id,
    #                         'qty': qty,
    #                         'sale_id': sale.id,
    #                     })
    #         return json.dumps({'message': 'Penjualan berhasil diperbarui'})
    #     return json.dumps({'error': 'Penjualan tidak ditemukan'})

    # @http.route('/api/sale/delete/<int:sale_id>', auth='public', methods=['DELETE'], csrf=False)
    # @serialize_exception
    # def delete_sale(self, sale_id, **kw):
    #     sale = request.env['new.sale'].sudo().browse(sale_id)
    #     if sale:
    #         sale.unlink()
    #         return json.dumps({'message': 'Penjualan berhasil dihapus'})
    #     return json.dumps({'error': 'Penjualan tidak ditemukan'})
