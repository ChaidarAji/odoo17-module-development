/** @odoo-module **/

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { onMounted, useRef, useState } from "@odoo/owl";


export class ShipLaterLinePopup extends AbstractAwaitablePopup {
    static template = "ah_pos_ship_later_line.ShipLaterLinePopup";
    setup() {
        super.setup();
        this.popup = useService("popup");
        this.state = useState({ shippingDate: this._today() });
        this.pos = usePos();
    }

    async confirmShipLaterQty() {
        var self = this;
        var order = self.pos.get_order();
        var orderlines = order.orderlines;

        const shipLaterLines = document.querySelectorAll('.ship_later_line');
        console.log(shipLaterLines);
        shipLaterLines.forEach(function (ship_later_line) {
            orderlines.forEach(function (line) {
                if (ship_later_line.dataset.line_id == line.id) {
                    console.log(ship_later_line.children);
                    if (ship_later_line.children[2].children[0].value > line.quantity) {
                        self.popup.add(ErrorPopup, {
                            title: _t("Input error"),
                            body: _t("The quantity to ship later is greater than the order quantity"),
                        });
                    } else {
                        line.to_ship_line_qty = parseInt(ship_later_line.children[2].children[0].value);
                    }
                }
            });
        });
        super.confirm();
    }

    getPayload() {
        return this.state.shippingDate < this._today() ? this._today() : this.state.shippingDate;
    }

    _today() {
        return new Date().toISOString().split("T")[0];
    }
}