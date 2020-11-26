# -*- coding: utf-8 -*-

from odoo import models, fields, api


class mymodule(models.Model):
    _inherit = 'pos.config'

    fixed_discount = fields.Boolean()
    restrict_pos_discount=fields.Many2many("res.partner", string=" Restrict Discount")

