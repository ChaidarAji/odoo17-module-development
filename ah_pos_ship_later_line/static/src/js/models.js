/** @odoo-module **/

import { Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, {

    constructor(attr, options) {
        this.to_ship_line_qty = this.to_ship_line_qty || 0.0;
    },

    set_to_ship_line_qty(to_ship_line_qty){
        this.to_ship_line_qty = to_ship_line_qty;
//            this.trigger('change',this);
    },

    export_as_JSON(){
            var json = super.export_as_JSON(...arguments);
            json.to_ship_line_qty = this.to_ship_line_qty;
        return json;
    },

    init_from_JSON(json){
        super.init_from_JSON(...arguments);
        this.to_ship_line_qty = json.to_ship_line_qty;
    },

    export_for_printing() {
        var lines = super.export_for_printing(...arguments);
        lines['to_ship_line_qty'] = this.to_ship_line_qty;
        return lines
    }
});
