/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { Component } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { parseFloat } from "@web/views/fields/parsers";
import { useService } from "@web/core/utils/hooks";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { usePos } from "@point_of_sale/app/store/pos_hook";


export class DepositTopupButton extends Component {
    static template = 'ah_customer_deposit.DepositTopupButton';

    setup() {
        super.setup();
        this.popup = useService("popup");
        this.pos = usePos()
    }
    
    async onClick() {      
        console.log('click');
        let value =  0
        const { confirmed, payload } = await this.popup.add(NumberPopup, {
            title: _t('Topup Amount'),
            startingValue: value,
            isInputSelected: true,
        });

        if (confirmed) {
            let product = this.pos.db.get_product_by_id(this.pos.config.deposit_product[0]);
            if(product){
                var order = this.pos.get_order();                    
                order.add_product(product, {
                    price: parseFloat(payload),
                    extras: {
                        price_manually_set: true,
                    },
                });
                order.set_is_deposit_order(true)
            }             
        }
    }
}

ProductScreen.addControlButton({
    component: DepositTopupButton,
    condition: function() {
        return this.pos.get_order().get_partner() && this.pos.config.enable_deposit;
    },
});