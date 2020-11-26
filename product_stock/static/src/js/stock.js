odoo.define('point_of_sale.StockProduct', function (require) {
"use strict";
//    const { Gui } = require('point_of_sale.Gui');
//    const ProductItem = require('point_of_sale.ProductItem');
//    const Registries = require('point_of_sale.Registries');

    var models = require('point_of_sale.models');


    models.load_fields('pos.product.product', ['qty_available']);
    console.log(this)

//});
//
//    console.log(models);
//    console.log("xxxxxxxxxxxx");
//    models.load_fields('product.product', 'qty_available');
////
//    models.load_models({
//        model: 'product.product',
//        fields: ['qty_avaliable',],

//        loaded: function (self, invoices) {
//          var invoices_ids = _.pluck(invoices, 'id');
//          self.prepare_invoices_data(invoices);
//          self.invoices = invoices;
//          self.db.add_invoices(invoices);
//          self.get_invoice_lines(invoices_ids);
//      }
});

