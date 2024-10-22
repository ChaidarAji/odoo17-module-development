/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { PaymentInterface } from "@point_of_sale/app/payment/payment_interface";

const paymentStatus = {
    PENDING: 'pending',
    RETRY: 'retry',
    WAITING: 'waiting',
    FORCE_DONE: 'force_done',
    WAITING_QRIS: 'waiting_deposit'
}


export class PaymentDeposit extends PaymentInterface {
    setup() {
        super.setup(...arguments);
        this.successEcr = false;
    }

    set_payment_line_status(status){
      const order = this.pos.get_order()
      let paymentLine = order.selected_paymentline;
      paymentLine.set_payment_status(status)
    }

    send_payment_request(cid) {                 
        const order = this.pos.get_order();
        if(!order.partner){
          // Gui.showPopup('ErrorPopup', { title: "Error", body: "Partner must selected" });          
          // this.set_payment_line_status(paymentStatus.RETRY);
          return Promise.reject();
        }
        super.send_payment_request(...arguments);
        this._reset_state();
        return this._deposit_pay(cid);
    }

    check_payment_deposit(){
      return this._deposit_check();
    }
    
    send_payment_cancel(order, cid) {
        this._super.apply(this, arguments);
        //this.pos_interface_conn.close();
        return Promise.resolve();
    }

    close() {
        this._super.apply(this, arguments);
    }

    _reset_state() {
        this.was_cancelled = false;
        this.remaining_polls = 4;
        clearTimeout(this.polling);
    }

    _handle_odoo_connection_failure(data) {
        // handle timeout
        const order = this.pos.get_order()
        let paymentLine = order.selected_paymentline;
        if (paymentLine) {
          paymentLine.set_payment_status(paymentStatus.RETRY)
        }
        this._show_error(_t('Could not connect to the Odoo server, please check your internet connection and try again.'))
        return Promise.reject(data) // prevent subsequent onFullFilled's from being called
      }

    async generate_deposit_change(amount){
      var self = this; 
      var values = {
        customer_id: this.pos.get_order().partner.id,
        type: 'change',
        debit: amount,
        order_id: this.pos.get_order().id,
        cashier_id: this.pos.get_cashier().id,
        note: this.pos.get_order().name
      }
      const result = await this.pos.orm.call('customer.deposit', 'create_from_ui', [values,values]);
      console.log('result',result);
      if(result){
        self.successEcr = true;
        this.pos.get_order().partner.remaining_deposit_amount = this.pos.get_order().partner.remaining_deposit_amount - amount;
      }
    }

    async get_remaining_deposit_amount(amount){
        var self = this; 
        if (this.pos.get_order().partner){
            const result = await this.pos.orm.call('res.partner', 'search_read', [
                [['id', '=', this.pos.get_order().partner.id]],
                ['remaining_deposit_amount']
            ]);
            if (result && result.length > 0) {
                const remaining_deposit_amount = result[0]['remaining_deposit_amount'];
                if (remaining_deposit_amount >= amount) {
                    await self.generate_deposit_change(amount);
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        } else {
            return false;
        }
    }
    
    async _deposit_pay() { 
        console.log('_deposit_pay');
        const self = this;
        const order = this.pos.get_order();
        let paymentLine = order.selected_paymentline;
        if (paymentLine && paymentLine.amount <= 0) {
          this._show_error(
            _t('Cannot process transaction with zero or negative amount.')
          )
          return Promise.resolve();
        }          
        var result = await this.get_remaining_deposit_amount(paymentLine.amount);
        if(!result){
          this._show_error(
            _t('Cannot process transaction , balance not sufficient.')
          )
          return Promise.resolve();
        }
        this.set_payment_line_status(paymentStatus.WAITING);        
        return this.start_get_status_polling();
      }
            
    
    _deposit_check(){
      console.log('_deposit_check');
      const self = this;
      const order = this.pos.get_order();
      let paymentLine = order.selected_paymentline;
      if (paymentLine && paymentLine.amount <= 0) {
        this._show_error(
          _t('Cannot process transaction with zero or negative amount.')
        )
        return Promise.resolve();
      }
      var data = this.generate_ecr_message('32', paymentLine);
      this.send_data_to_web_socket(data);
      this.set_payment_line_status(paymentStatus.WAITING);    
      return this.start_get_status_polling();
    }

    start_get_status_polling () {
        const self = this
        const res = new Promise(function (resolve, reject) {
          clearTimeout(self.polling)
          self._poll_for_response(resolve, reject)
          self.polling = setInterval(function () {
            self._poll_for_response(resolve, reject)
          }, 5500)
        })
  
        // make sure to stop polling when we're done
        res.finally(function () {
          self._reset_state()
        })
  
        Promise.resolve()
        return res
    }

    _poll_for_response(resolve, reject) {
        const self = this
        
        if (this.was_cancelled) {
          resolve(false)
          return Promise.resolve()
        }
  
        const order = this.pos.get_order()
        const paymentLine = order.selected_paymentline;

  
        // If the payment line dont have xendit invoice then stop polling retry.
        if (!paymentLine) {
          resolve(false)
          return Promise.resolve()
        }

        // if (this.counter == 10){
        //   this.counter = 0;
        //   console.log(this.counter);
        //   resolve(true)
        //   return Promise.resolve()
        // }
        // this.counter = this.counter + 1;

        if(this.successEcr){
          this.successEcr = false;
          resolve(true);
          return Promise.resolve();
        }
    }  
};