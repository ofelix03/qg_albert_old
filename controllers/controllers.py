# -*- coding: utf-8 -*-
from odoo import http

# class QgAlbert(http.Controller):
#     @http.route('/qg_albert/qg_albert/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/qg_albert/qg_albert/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('qg_albert.listing', {
#             'root': '/qg_albert/qg_albert',
#             'objects': http.request.env['qg_albert.qg_albert'].search([]),
#         })

#     @http.route('/qg_albert/qg_albert/objects/<model("qg_albert.qg_albert"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('qg_albert.object', {
#             'object': obj
#         })