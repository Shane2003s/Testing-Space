/** @odoo-module */
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
patch(PosStore.prototype, {
	getReceiptHeaderData() {
		var result=super.getReceiptHeaderData()
		result["pos_logo_base_64"]=this.pos_logo_base_64
		result["show_logo_on_receipt"]=this.config.show_logo_on_receipt
		return result
	}
});
patch(Navbar.prototype, {
	get_logo() {
		var self = this;
		if (self.pos && self.pos.config && !self.pos.config.pos_logo)
			return false;
		var img = new Image();
		img.onload = function () {
			var ratio = 1;
			var targetwidth = 300;
			var maxheight = 150;
			if (img.width !== targetwidth) {
				ratio = targetwidth / img.width;
			}
			if (img.height * ratio > maxheight) {
				ratio = maxheight / img.height;
			}
			var width = Math.floor(img.width * ratio);
			var height = Math.floor(img.height * ratio);
			var c = document.createElement('canvas');
			c.width = width;
			c.height = height;
			var ctx = c.getContext('2d');
			ctx.drawImage(img, 0, 0, width, height);
			self.pos.pos_logo_base_64 = c.toDataURL();
		};
		if (self.pos && self.pos.config && self.pos.config.id) {
			img.src = window.location.origin + '/web/image?model=pos.config&field=pos_logo&id=' + self.pos.config.id;
			return window.location.origin + '/web/image?model=pos.config&field=pos_logo&id=' + self.pos.config.id
		}
		else
			return false
	},
});


