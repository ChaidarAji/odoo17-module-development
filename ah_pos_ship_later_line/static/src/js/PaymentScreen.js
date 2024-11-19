/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { ShipLaterLinePopup } from "./ShipLaterLinePopup";


patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.popup = useService("popup");
        console.log(this.currentOrder.orderlines);
    },

    async toggleShippingDatePicker() {
        if (!this.currentOrder.getShippingDate()) {
            const shipLaterLinesConfirmed = await this.selectShipLaterLines();
            console.log(shipLaterLinesConfirmed);
            if (shipLaterLinesConfirmed.confirmed) {
                this.currentOrder.setShippingDate(shipLaterLinesConfirmed.payload);
            }
        } else {
            this.currentOrder.setShippingDate(false);
        }
    },

    async selectShipLaterLines() {
        // click_ship
        var orderlines = this.currentOrder.orderlines
        var lines=[]
        for (let i=0; i<orderlines.length; i++){
            lines.push({'id': orderlines[i].id,
                        'product_name': orderlines[i].full_product_name || orderlines[i].product.display_name,
                        'quantity': orderlines[i].quantity,
                        'to_ship_line_qty': orderlines[i].to_ship_line_qty})
        }
        const confirmed = await this.popup.add(ShipLaterLinePopup, {
            orderline: lines});
        return confirmed;
    },


    async validateOrder(isForceValidate) {
        var self = this;
        var orderlines = this.currentOrder.orderlines;
        var overqty = false;
        orderlines.forEach(function(line){
            if(line.quantity>0 && line.quantity<line.to_ship_line_qty){
                overqty = true
            }
        });
        if (overqty){
            self.showPopup('ErrorPopup', {
                title: "Ship Later Lines",
                body: "There is ship later qty. more than order qty. Please correct it First!",
            });
            return;
        }else{
            super.validateOrder(isForceValidate);
        }
    }

});