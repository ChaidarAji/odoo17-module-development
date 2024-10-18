/** @odoo-module **/

import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";


patch(OrderReceipt.prototype,{
    setup() {
        super.setup();
        this.pos = usePos();
        this.order = this.pos.get_order();
    },

    get_is_deposit_order(){
        return this.order.get_is_deposit_order();            
    },
    
    get_remaining_deposit_amount() {
        return this.order.get_partner().remaining_deposit_amount;
    }
});