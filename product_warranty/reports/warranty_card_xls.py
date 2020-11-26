from odoo import models

class warrantyXlsx(models.AbstractModel):
    _name = 'report.product_warranty.warranty_report_details_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        main_heading = workbook.add_format({'font_size': 14, 'align': 'vjustify', 'bold': True, 'bg_color': '#c5d4c9'})
        table_heading = workbook.add_format({'font_size': 12, 'align': 'vjustify', 'bold': True, 'bg_color': '#c5d4c9'})
        product_name = workbook.add_format({'font_size': 12, 'align': 'left', 'bold': True, 'bg_color': '#9bd8e0'})
        table_contents = workbook.add_format({'font_size': 10, 'align': 'vjustify','bold': True,})
        sheet = workbook.add_worksheet('Warranty Report')
        # print("print data", data)

        sheet.set_column(5, 5, 30)
        sheet.set_column(4, 4, 30)
        sheet.set_column(6, 6, 15)
        sheet.set_column(7, 7, 15)
        sheet.set_column(8, 8, 15)
        # sheet.set_column(1, 8, 15)

        sheet.write(4, 5, 'Warranty Report', main_heading)
        sheet.write(6, 3, 'S NO.', table_heading)
        sheet.write(6, 4, 'Product', table_heading)
        sheet.write(6, 5, 'Invoice', table_heading)
        sheet.write(6, 6, 'Customer', table_heading)
        sheet.write(6, 7, 'Warranty Date', table_heading)
        sheet.write(6, 8, 'Status', table_heading)

        print("print data", data['warranty_ids'])

        row=7
        column=4
        product_row = 7
        product_colum =4
        c=0
        sl_no=product_colum-1
        i=1
        s=chr(97)
        print(s)

        for doc in data['warranty_ids']:
            print("print list", doc['product'])
            # for rec in doc['details']:
            if doc['product']:
                sheet.write(product_row, sl_no, i, product_name)
                sheet.write(product_row, product_colum, doc['product'], product_name)


            row = row + 1
            for pro in doc['details']:
                print("pro", pro)
                sheet.write(row, 3,s, table_heading)

                if pro['invoice']:
                    sheet.write(row, 5, pro['invoice'], table_contents)
                if pro['customer']:
                    sheet.write(row, 6, pro['customer'], table_contents)
                if pro['expiry']:
                    sheet.write(row, 7, pro['expiry'], table_contents)
                if pro['status']:
                    sheet.write(row, 8, pro['status'], table_contents)
                row = row + 1
                c=c+2
                print("row",row)
                i=i+1
                s=chr(ord(s) + 1)

            product_row=product_row+c




