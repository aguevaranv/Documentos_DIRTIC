# -*- coding: utf-8 -*-
# from odoo import http


# class Gestionoperativa(http.Controller):
#     @http.route('/gestionoperativa/gestionoperativa', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestionoperativa/gestionoperativa/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestionoperativa.listing', {
#             'root': '/gestionoperativa/gestionoperativa',
#             'objects': http.request.env['gestionoperativa.parteopeavidetalle'].search([]),
#         })

#     @http.route('/gestionoperativa/gestionoperativa/objects/<model("gestionoperativa.parteopeavidetalle"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestionoperativa.object', {
#             'object': obj
#         })
