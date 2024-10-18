/** @odoo-module **/

import { models, Order, Payment } from "@point_of_sale/app/store/models";
import {PaymentDeposit} from '@ah_customer_deposit/js/payment_deposit';
import { register_payment_method } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";

register_payment_method('deposit', PaymentDeposit);

patch(Order.prototype, {

    constructor(obj, options) {
        this.is_deposit_order = this.is_deposit_order || false;                
    },

    set_is_deposit_order(is_deposit_order){
        this.is_deposit_order = is_deposit_order
    },

    get_is_deposit_order(){
        return this.is_deposit_order;
    },

    add_product(product, options){
        if(this.get_is_deposit_order()){
            return
        }
        super.add_product(product,options);
    },

    remove_orderline( line ){        
        super.remove_orderline(line);
        if(this.orderlines.length == 0 && this.get_is_deposit_order()){
            this.set_is_deposit_order(false);
        }
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.is_deposit_order = json.is_deposit_order
    },
    
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.is_deposit_order = this.is_deposit_order
        return json;
    },
    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        result.is_deposit_order = this.is_deposit_order;
        if (this.get_partner()) {
            result.partner = this.get_partner();
        }
        return result;
    },
    clone(){
        const order = super.clone(...arguments);
        order.is_deposit_order = json.is_deposit_order
        return order;
    },
    add_paymentline(payment_method) {
        this.assert_editable();
        if (this.electronic_payment_in_progress()) {
            return false;
        } else {
            var newPaymentline = new Payment(
                { env: this.env },
                { order: this, payment_method: payment_method, pos: this.pos }
            );
            this.paymentlines.add(newPaymentline);
            this.select_paymentline(newPaymentline);
            if(this.pos.config.cash_rounding){
                this.selected_paymentline.set_amount(0);
            }
            console.log("1111111111111111111",payment_method);
            if (payment_method.use_payment_terminal=='deposit'){
                if (this.partner.remaining_deposit_amount>=this.get_due()){
                    newPaymentline.set_amount(this.get_due());
                }else{
                    newPaymentline.set_amount(this.partner.remaining_deposit_amount);
                }
            }else {
                newPaymentline.set_amount(this.get_due());
            }

            if (payment_method.payment_terminal) {
                newPaymentline.set_payment_status('pending');
            }
            return newPaymentline;
        }
    }
})


patch(Payment.prototype,{
    constructor(obj, options) {
        this.terminal_id = this.terminal_id || '';
    },
    
    set_terminal_id(terminal_id){
        this.terminal_id = terminal_id;
    },
    
    init_from_JSON(json){
        this.terminal_id = json.terminal_id;
        super.init_from_JSON(...arguments);
    },
    
    export_as_JSON(){
        var json = super.export_as_JSON();            
        json.terminal_id = this.terminal_id;            
        return json;
    },
    
    clone(){
        var payment = super.clone();
        payment.terminal_id = this.terminal_id;
        return payment;
    }
})