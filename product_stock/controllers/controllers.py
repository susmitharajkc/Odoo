# -*- coding: utf-8 -*-
# from odoo import http


# class ProductStock(http.Controller):
#     @http.route('/product_stock/product_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_stock/product_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_stock.listing', {
#             'root': '/product_stock/product_stock',
#             'objects': http.request.env['product_stock.product_stock'].search([]),
#         })

#     @http.route('/product_stock/product_stock/objects/<model("product_stock.product_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_stock.object', {
#             'object': obj
#         })
