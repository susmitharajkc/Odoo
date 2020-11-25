# -*- coding: utf-8 -*-

from odoo import models, fields, api


class product_stock(models.Model):
    _inherit = 'pos.config'

    stocks = fields.Boolean()
