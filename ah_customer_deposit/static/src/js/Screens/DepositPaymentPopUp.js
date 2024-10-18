/** @odoo-module **/

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";


export class DepositPaymentPopUp extends AbstractAwaitablePopup {
    static template = 'ah_customer_deposit.DepositPaymentPopUp';
    static defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
    };
    setup() {
        super.setup();
        const NumberBuffer = useService("number_buffer");
        NumberBuffer.use(this._getNumberBufferConfig);
        // useListener("deposit_payment_confirm", this.deposit_payment_confirm);
    };
    async deposit_payment_confirm({ detail: paymentMethod }){
        let result = this.pos.get_order().add_paymentline(paymentMethod);
        if (result){
            NumberBuffer.reset();
            this.confirm()
            return true;
        }
        else{
            this.showPopup('ErrorPopup', {
                title: _t('Error'),
                body: _t('There is already an electronic payment in progress.'),
            });
            return false;
        }
    }

}