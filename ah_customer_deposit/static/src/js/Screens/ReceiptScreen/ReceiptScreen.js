/** @odoo-module **/

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

patch(ReceiptScreen.prototype, {
    setup() {
        // Call the parent setup method
        super.setup(); // Use super instead of _super
        this.rpc = useService('rpc'); // Use the rpc service
        this.get_remaining_deposit_amount(); // Call the method
        console.log("this.get_remaining_deposit_amount() called");
    },
    
    async get_remaining_deposit_amount() {
        const order = this.pos.get_order();
        if (order && order.get_partner()) {
            try {
                const result = await this.rpc({
                    model: "res.partner",
                    method: "search_read",
                    domain: [['id', '=', order.get_partner().id]],
                    fields: ['remaining_deposit_amount']
                });
                
                console.log("result", result);
                if (result && result.length > 0) {   
                    let new_partner = _.extend(order.get_partner(), result[0]);
                    console.log("new_partner", new_partner);
                    this.env.pos.db.add_partners(new_partner);                                                 
                }
            } catch (error) {
                console.error("RPC call failed:", error);
            }
        }
    }
});
