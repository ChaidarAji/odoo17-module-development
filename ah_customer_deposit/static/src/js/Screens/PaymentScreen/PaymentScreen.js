/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { onMounted } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { useService } from "@web/core/utils/hooks";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { formatMonetary } from "@web/views/fields/formatters";
import { usePos } from "@point_of_sale/app/store/pos_hook";



patch(PaymentScreen.prototype, {
    setup() {   
        super.setup();
        this.popup = useService("popup");
        this.pos = usePos()
        const NumberBuffer = useService("number_buffer");
        NumberBuffer.use(this._getNumberBufferConfig);
        console.log('number buffer',NumberBuffer);
        onMounted(() => {
            const pendingPaymentLine = this.currentOrder.paymentlines.find(
                paymentLine => paymentLine.payment_method.use_payment_terminal === 'deposit' &&
                    (!paymentLine.is_done() && paymentLine.get_payment_status() !== 'pending')
            );
            if (pendingPaymentLine) {    
                const paymentTerminal = pendingPaymentLine.payment_method.payment_terminal;
                if(pendingPaymentLine.get_payment_status() != 'waiting_deposit'){                
                    pendingPaymentLine.set_payment_status('waiting');
                    paymentTerminal.start_get_status_polling().then(isPaymentSuccessful => {
                        if (isPaymentSuccessful) {
                            pendingPaymentLine.set_payment_status('done');
                            pendingPaymentLine.can_be_reversed = paymentTerminal.supports_reversals;
                        } else {
                            pendingPaymentLine.set_payment_status('retry');
                        }
                    });
                }
            }
        });
    },

    async _checkDepositPayment(line){
        const payment_terminal = line.payment_method.payment_terminal;
        line.set_payment_status('waiting');
        const isPaymentSuccessful = await payment_terminal.check_payment_deposit(line.cid);
        if (isPaymentSuccessful) {
            line.set_payment_status('done');
            line.can_be_reversed = payment_terminal.supports_reversals;
            if (
                this.currentOrder.is_paid() &&
                utils.float_is_zero(this.currentOrder.get_due(), this.pos.currency.decimal_places)
            ) {
                this.trigger('validate-order');
            }
        } else {
            line.set_payment_status('waiting_deposit');
        }
    },

    async addNewPaymentLine(paymentMethod) {
        if (paymentMethod.use_payment_terminal == 'deposit'){
            if (!this.currentOrder.partner){
                this.popup.add(ErrorPopup, {
                    title: _t('Error'),
                    body: _t('Please Set the Customer!'),
                });
            }else{
                if (!this.currentOrder.partner.remaining_deposit_amount){
                    this.popup.add(ErrorPopup, {
                        title: _t('Error'),
                        body: _t('This customer does not have remaining deposit!'),
                    });
                }else {
                    const {confirmed, payload} = await this.popup.add(ConfirmPopup, {
                        title: _t('Payment Deposit'),
                        body: _t('Remaining Deposit : ')+formatMonetary(this.currentOrder.partner.remaining_deposit_amount, { currencyId: this.pos.currency.id }),
                    });
                    console.log('confirm',confirmed);
                    if (confirmed){
                        super.addNewPaymentLine(paymentMethod);
                    }
                }
            }
        }
        else{
            super.addNewPaymentLine(paymentMethod);
        }
    }
    
});