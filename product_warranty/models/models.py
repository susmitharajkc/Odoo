from odoo import models, fields, api
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError

class product_warranty(models.Model):
    
    _name = 'product_warranty.product_warranty'
    _rec_name = 'warranty_number'
    warranty_number = fields.Char('Warranty Number',readonly=True, required=True, copy=False, default= 'NEW')
    invoice = fields.Many2one('account.move', 'Invoice')
    partner_id = fields.Many2one("res.partner",string='Customer',
                              related='invoice.partner_id',store=True)

    product = fields.Many2one("product.product", string='Product')
    invoice_date = fields.Date('Invoice date', related='invoice.invoice_date')
    serial_number = fields.Many2one("stock.production.lot", string='Serial number')
    request_date = fields.Date('Current date', default=fields.Date.today())
    expiry_date = fields.Date('Expiry date')
    state = fields.Selection([('draft', 'Draft'),
                              ('to approve', 'To Approve'),
                              ('approved', 'Approved'),
                              ('received', 'Received'),
                              ('return', 'Done'),
                              ('cancelled', 'Cancelled'),
                              ], required=True, default='draft')

# autofill the partner address..............................................................
#
#     @api.onchange('partner_id')
#     def onchange_partner(self):
#         for rec in self:
#             return

# get the expiry date...........................................................................

    @api.onchange('product')
    def compute_expiry(self):
        if self.invoice_date != False:
            expiry_calculate = self.invoice.invoice_date + timedelta(days=self.product.warranty_periods)
            self.write({'expiry_date': expiry_calculate})
        for rec in self:
            return{'domain': {'serial_number': [('product_id', '=', rec.product.id)]}}

# generate the warranty number.................................................................

    @api.model
    def create(self, vals):
        if vals.get('warranty_number', 'New') == 'New':
            vals['warranty_number'] = self.env['ir.sequence'].next_by_code(
                'warranty.number') or 'New'
        result = super(product_warranty, self).create(vals)
        return result

# define the states......................................................................

    def button_reset(self):
        for rec in self:
            rec.state = 'draft'

    def button_to_approve(self):
        for rec in self:
            rec.write({'state': 'to approve'})

# operation based on approved...................................................................

    def button_approved(self):
        """state is approved"""
        for rec in self:
            rec.write({'state': 'received'})

        product_location=self.env['stock.quant'].search([('product_id','=',self.product.id),
                                                         ('location_id','!=',[14,40,5])])

        # stock move when warranty type is replacement warranty
        if self.product.warranty_type == 'replacement_warranty':
            self.env['stock.picking'].create({
                'location_id':self.env.ref('stock.stock_location_customers').id,
                'location_dest_id': 18,
                'picking_type_id': self.env.ref('stock.picking_type_in').id,
                'partner_id': self.partner_id.id,
                'origin':self.warranty_number,
                'state':'done',
                'move_ids_without_package': [(0, 0, {
                    'name': 'name',
                    'location_id':self.env.ref('stock.stock_location_customers').id,
                    'location_dest_id': 18,
                    'picking_type_id': self.env.ref('stock.picking_type_in').id,
                    'product_id': self.product.id,
                    'product_uom': self.product.uom_id.id,
                    'state':'done',
                    'product_uom_qty': 1,
                    'quantity_done': 1
                })],


            })
            move=self.env['stock.move'].create({
                'name':self.warranty_number,
                'location_id':self.env.ref('stock.stock_location_customers').id,
                'location_dest_id': 18,
                'product_id':self.product.id,
                'product_uom':self.product.uom_id.id,
                'product_uom_qty':1,
                'reference':self.warranty_number,
                'state':'done'
            })
            move._action_confirm()
            move._action_confirm()
            move.move_line_ids.write(
                {'qty_done':1}
            )
            move._action_done()
        else:
                    # stock move when warranty type is service warranty
            self.env['stock.picking'].create({
                'location_id': self.env.ref('stock.stock_location_customers').id,
                'location_dest_id': 40,
                'picking_type_id': self.env.ref('stock.picking_type_in').id,
                'partner_id': self.partner_id.id,
                'origin': self.warranty_number,
                'state':'done',
                'move_ids_without_package': [(0, 0, {
                    'name': 'name',
                    'location_id': self.env.ref('stock.stock_location_customers').id,
                    'location_dest_id': 40,
                    'picking_type_id': self.env.ref('stock.picking_type_in').id,
                    'product_id': self.product.id,
                    'product_uom': self.product.uom_id.id,
                    'state':'done',
                    'product_uom_qty': 1,
                    'quantity_done': 1
                })],
            })

            self.env['stock.move'].create({
                'name': self.warranty_number,
                'location_id': self.env.ref('stock.stock_location_customers').id,
                'location_dest_id': 40,
                'product_id': self.product.id,
                'product_uom': self.product.uom_id.id,
                'product_uom_qty': 1,
                'reference': self.warranty_number,
                'state':'done'
            })
    def button_return(self):
        """function for return product button"""
        for rec in self:
            rec.write({'state': 'return'})
        self.env['stock.picking'].create({
                    'location_id': 40,
                    'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                    'picking_type_id': self.env.ref('stock.picking_type_out').id,
                    'partner_id': self.partner_id.id,
                    'origin': self.warranty_number,
                    'state': 'done',
                    'move_ids_without_package': [(0, 0, {
                        'name': 'name',
                        'location_id': 40,
                        'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                        'picking_type_id': self.env.ref('stock.picking_type_out').id,
                        'product_id': self.product.id,
                        'product_uom': self.product.uom_id.id,
                        'state': 'done',
                        'product_uom_qty': 1,
                        'quantity_done': 1
                    })],

                })

        move = self.env['stock.move'].create({
                    'name': self.warranty_number,
                    'location_id': 40,
                    'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                    'product_id': self.product.id,
                    'product_uom': self.product.uom_id.id,
                    'product_uom_qty': 1,
                    'reference': self.warranty_number,
                    'state': 'done'
                })
        move._action_confirm()
        move._action_confirm()
        move.move_line_ids.write(
                    {'qty_done': 1}
                )
        move._action_done()


    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancelled'})

# function for filling product field while selecting invoice....................................................

    @api.onchange('invoice','expiry_date')
    def onchange_invoice(self):
        pro=[]
        for rec in self.invoice.invoice_line_ids:
            pro.append(rec.product_id.id)
            if self.expiry_date and self.request_date:
                if self.expiry_date <= self.request_date:
                    raise ValidationError("Warranty Period Of This Product Has Been Expired!")
        return {'domain':{'product':[('id','in',pro),('warranty','=',True)]}}


#  stock move smart button in warranty request.........................................................

    def get_stock_move(self):
        self.ensure_one()

        return {
             'type': 'ir.actions.act_window',
            'name': 'Stock Move',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.move',
            'domain': [('name', '=', self.warranty_number)],
            'context': "{'create': False}"
        }

# inherit from product form to add a field...................................

class product_template(models.Model):
        _inherit = 'product.template'

        warranty_periods = fields.Integer(string='Warranty Period')

# get count in smart button...................................................

class search(models.Model):
    _inherit = 'account.move'
    warranty_details = fields.One2many('product_warranty.product_warranty', 'invoice', string='Warranty Info')
    warranty_count = fields.Integer(compute='compute_count')

    def compute_count(self):
            for record in self:
                    record.warranty_count = self.env['product_warranty.product_warranty'].search_count(
                            [('invoice', '=', self.id)])

# warranty smart button in invoice................................................................
    def get_warranty(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Warranty Requests',
            'view_mode': 'tree',
            'res_model': 'product_warranty.product_warranty',
            'domain': [('invoice', '=', self.id)],
            'context': "{'create': False}"
        }

# model for inheriting warranty period field...........................................................

class warranty_period_inherit(models.Model):
        _inherit = 'product.template'
        warranty_type = fields.Selection(selection=[
            ('replacement_warranty', 'Replacement Warranty'),
            ('services_warranty', 'Services Warranty')],
            string='Warranty Type')
        warranty = fields.Boolean('Warranty', default=False)

