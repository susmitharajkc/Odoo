from odoo import models, fields, api
from odoo.exceptions import MissingError
from datetime import datetime
import numpy as np

class wizard(models.TransientModel):
    _name = 'warranty.wizard'

    warranty_product = fields.Many2many('product.product', string='Warranty Products')
    # request_date = fields.Date("Current Date", default=datetime.today())
    warranty_from_date = fields.Date('From')
    warranty_to_date = fields.Date('To')

    def Print_pdf(self):
        if self.warranty_product:
            products = []
            products_name = []
            if self.warranty_product and self.warranty_from_date and self.warranty_to_date:
                for rec in self.warranty_product:
                    products.append(rec.id)
                    products_name.append(rec.name)
                    print("products_name", products_name)
                    print("products", products)
                    products_list = tuple(products)
                    print("product list", products_list)
                    self.env.cr.execute(
                        "SELECT * FROM product_warranty_product_warranty WHERE "
                        "product in %s AND request_date >= %s ""AND request_date <= ""%s ",
                        (products_list, self.warranty_from_date, self.warranty_to_date,))
                    warranty_ids = self.env.cr.fetchall()
                    print("WARRANRY IDS ", warranty_ids)


            elif self.warranty_from_date and not self.warranty_to_date:
                for rec in self.warranty_product:
                    products.append(rec.id)
                    products_list = tuple(products)
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE product"
                                    " in %s AND request_date >= %s",
                                    (products_list, self.warranty_from_date))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)

            elif not self.warranty_from_date and self.warranty_to_date:
                for rec in self.warranty_product:
                    products.append(rec.id)
                    products_list = tuple(products)
                self.env.cr.execute(
                    "SELECT * FROM product_warranty_product_warranty WHERE product in %s AND request_date <= %s",
                    (products_list, self.warranty_to_date))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)

            else:
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE product = %s",
                                    (self.warranty_product.id,))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)

        elif self.warranty_from_date:
                # (0,1,1)
                if self.warranty_to_date:
                    self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE request_date >= %s AND "
                                        "request_date <= %s",
                                        (self.warranty_from_date, self.warranty_to_date))
                    warranty_ids = self.env.cr.fetchall()
                    print(warranty_ids)
                else:
                    self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE request_date >= %s",
                                        (self.warranty_from_date,))
                    warranty_ids = self.env.cr.fetchall()
                    print(warranty_ids)
        else:
                # (0,1,0)
                if self.warranty_to_date:
                    self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE request_date <= %s",
                                        (self.warranty_to_date,))
                    warranty_ids = self.env.cr.fetchall()
                    print(warranty_ids)
                else:
                    # (0,0,0)
                    self.env.cr.execute("SELECT * FROM product_warranty_product_warranty")
                    warranty_ids = self.env.cr.fetchall()


        if not warranty_ids:
                    raise MissingError("No warranty request had been found ")
        else:
                    p_name= []
                    for id in warranty_ids:
                        p_name.append(id[4])
                    names = np.unique(p_name)
                    pro = []
                    for rec in names:
                        print("pro ", rec)
                        leaves = []
                        for id in warranty_ids:
                            if id[4]== rec:

                                self.env.cr.execute("SELECT name FROM product_template WHERE id in "
                                                    "(SELECT product_tmpl_id FROM product_product WHERE id in "
                                                    "(SELECT product FROM product_warranty_product_warranty"
                                                    " WHERE product = %s))",
                                                    (id[4],))
                                products = self.env.cr.fetchall()
                                print(products)
                                self.env.cr.execute("SELECT invoice_payment_ref FROM account_move WHERE id in "
        
                                                    "(SELECT invoice FROM product_warranty_product_warranty "
                                                    "WHERE invoice = %s)", (id[2],))
                                invoice = self.env.cr.fetchall()
                                print(invoice)
                                self.env.cr.execute("SELECT name FROM res_partner WHERE id in"
                                                    "(SELECT partner_id FROM product_warranty_product_warranty"
                                                    " WHERE partner_id= %s)",
                                                    (id[3],))
                                customer = self.env.cr.fetchall()
                                product = products
                                invoice = invoice[0][0]
                                customer = customer
                                expiry = id[7]
                                status = id[8]
                                leaves.append({
                                    'invoice': invoice,
                                    'customer': customer[0][0],
                                    'expiry': expiry,
                                    'status': status
                                })

                        pro.append({
                                'product': products[0][0],
                                'details': leaves
                        })

                    data = {'model': 'warranty.wizard',
                            'from_date': self.warranty_from_date,
                            'to_date': self.warranty_to_date,
                            'warranty_ids': pro}
                    print("final data", data)
                    return self.env.ref('product_warranty.warranty_reporting').report_action(self, data=data)

    def Print_xls(self):
        products = []
        products_name = []
        if self.warranty_product and self.warranty_from_date and self.warranty_to_date:
            for rec in self.warranty_product:
                products.append(rec.id)
                products_name.append(rec.name)
                print("products_name", products_name)
                print("products", products)
                products_list = tuple(products)
                print("product list", products_list)
                self.env.cr.execute(
                    "SELECT * FROM product_warranty_product_warranty WHERE "
                    "product in %s AND request_date >= %s ""AND request_date <= ""%s ",
                    (products_list, self.warranty_from_date, self.warranty_to_date,))
                warranty_ids = self.env.cr.fetchall()
                print("WARRANRY IDS ", warranty_ids)
        elif self.warranty_from_date and not self.warranty_to_date:
                for rec in self.warranty_product:
                    products.append(rec.id)
                    products_list = tuple(products)
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE product"
                                    " in %s AND request_date >= %s",
                                    (products_list, self.warranty_from_date))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)

        elif not self.warranty_from_date and self.warranty_to_date:
                for rec in self.warranty_product:
                    products.append(rec.id)
                    products_list = tuple(products)
                self.env.cr.execute(
                    "SELECT * FROM product_warranty_product_warranty WHERE product in %s AND request_date <= %s",
                    (products_list, self.warranty_to_date))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)
        else:
            self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE product = %s",
                                (self.warranty_product.id,))
            warranty_ids = self.env.cr.fetchall()
            print(warranty_ids)

        p_name = []
        for id in warranty_ids:
            p_name.append(id[4])
        names = np.unique(p_name)
        pro = []
        for rec in names:
            print("pro ", rec)
            leaves = []
            for id in warranty_ids:
                if id[4] == rec:
                    self.env.cr.execute("SELECT name FROM product_template WHERE id in "
                                        "(SELECT product_tmpl_id FROM product_product WHERE id in "
                                        "(SELECT product FROM product_warranty_product_warranty"
                                        " WHERE product = %s))",
                                        (id[4],))
                    products = self.env.cr.fetchall()
                    print(products)
                    self.env.cr.execute("SELECT invoice_payment_ref FROM account_move WHERE id in "

                                        "(SELECT invoice FROM product_warranty_product_warranty "
                                        "WHERE invoice = %s)", (id[2],))
                    invoice = self.env.cr.fetchall()
                    print(invoice)
                    self.env.cr.execute("SELECT name FROM res_partner WHERE id in"
                                        "(SELECT partner_id FROM product_warranty_product_warranty"
                                        " WHERE partner_id= %s)",
                                        (id[3],))
                    customer = self.env.cr.fetchall()
                    product = products
                    invoice = invoice[0][0]
                    customer = customer
                    expiry = id[7]
                    status = id[8]
                    leaves.append({
                        'invoice': invoice,
                        'customer': customer[0][0],
                        'expiry': expiry,
                        'status': status
                    })

            pro.append({
                'product': products[0][0],
                'details': leaves
            })

        data = {'model': 'warranty.wizard',

                'from_date': self.warranty_from_date,
                'to_date': self.warranty_to_date,
                'warranty_ids': pro}

        return self.env.ref('product_warranty.warranty_report_details_xls').report_action(self, data)
