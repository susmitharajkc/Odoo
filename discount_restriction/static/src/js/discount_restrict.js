odoo.define('point_of_sale.RestrictDiscount', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    var models = require('point_of_sale.models');

    models.load_fields('product.product', 'qty_available');
//    console.log(this)

    class RestrictDiscount extends PosComponent {
         constructor() {
                super(...arguments);
                useListener('restrict_discount', this.restrict_discount);
            }
        async restrict_discount() {
            var num=20
            console.log(this)

            var pos_customer = this.env.pos.attributes.selectedClient
            var pos_config_customer = this.env.pos.config.restrict_pos_discount[0]
            console.log(pos_customer)
            console.log(pos_config_customer)
            if (!pos_customer){
                console.log("hello world")
                alert("SELECT THE CUSTOMER")
                }


            else if(pos_customer.id == pos_config_customer ){


                this.showPopup('ErrorPopup', {
                    title : this.env._t("SORRY your discount is RESTRICTED"),

                    });
               }
            else{
                var self = this;
                const { confirmed, payload } = await this.showPopup('NumberPopup',{
                    title: this.env._t('Discount Amount'),
                    startingValue: this.env.pos.config.discount_percentage,
                });
                if (confirmed) {
                    const val = (payload);
                    await self.apply_discount(val);
                    console.log("vals",this.val);
                    console.log(payload);


                }
                }
               }

            async apply_discount(pc) {

            var order    = this.env.pos.get_order();
            var lines    = order.get_orderlines();
            var product  = this.env.pos.db.get_product_by_id(this.env.pos.config.discount_product_id[0]);
            if (product === undefined) {
                await this.showPopup('ErrorPopup', {
                    title : this.env._t("No discount product found"),
                    body  : this.env._t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
                });
                return;
            }

//            // Remove existing discounts
//            var i = 0;
//            while ( i < lines.length ) {
//                if (lines[i].get_product() === product) {
//                    order.remove_orderline(lines[i]);
//                } else {
//                    i++;
//                }
//            }

            // Add discount
            // We add the price as manually set to avoid recomputation when changing customer.
            var base_to_discount = order.get_total_without_tax();
            if (product.taxes_id.length){
                var first_tax = this.pos.taxes_by_id[product.taxes_id[0]];
                if (first_tax.price_include) {
                    base_to_discount = order.get_total_with_tax();
                }
            }
            var discount = - pc / 100.0 * base_to_discount;


            if( discount < 0 ){
                order.add_product(product, {
                    price: discount,
                    lst_price: discount,
                    extras: {
                        price_manually_set: true,
//                    console.log(discount_percentage)
                    },
                });
            }
        }



    }



    RestrictDiscount.template = 'RestrictDiscount';

    ProductScreen.addControlButton({
        component: RestrictDiscount,
        condition: function() {
            return this.env.pos.config.module_pos_discount && this.env.pos.config.discount_product_id;
        },
    });
    Registries.Component.add(RestrictDiscount);

    return RestrictDiscount;
});




