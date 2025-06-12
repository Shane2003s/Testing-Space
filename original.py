from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TAKSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sale_multi_uom_unit = fields.Char(
        string="Inventory Unit", compute="_compute_sale_uom_unit", readonly=False, store=True)
    sale_order_remark = fields.Char(string='Sale Order Remark', trim=True)
    commission = fields.Float(string="Commission %")
    commission_amount = fields.Monetary(
        string='Commission Amount', compute='_compute_amount',
        store=True, precompute=True)
    brand_id = fields.Many2one(
        'product.category', string='Brand', related='product_id.categ_id.parent_id', store=True)
    customer_remark = fields.Char(string='Customer Remark', trim=True)

    @api.onchange('product_uom_qty')
    def _compute_sale_uom_unit(self):
        for record in self:
            for rec in record.product_id:
                if record.product_uom_qty:

                    # check product stock qty
                    record.check_product_stock_qty(
                        product_id=record.product_id, product_uom_qty=record.product_uom_qty)

                    residual_qty = record.product_uom_qty
                    loop_value = 1
                    final_uom_unit = []
                    if rec.packaging_ids:
                        while loop_value > 0:
                            packaging_quantities = [
                                packaging_record.qty for packaging_record in rec.packaging_ids if packaging_record.qty <= residual_qty]
                            if packaging_quantities:
                                closest_value = max(packaging_quantities)
                            else:
                                closest_value = None
                                break

                            if closest_value:
                                for package_uom in rec.packaging_ids:
                                    if package_uom.qty == closest_value:
                                        package_name = package_uom.package_type_id.name

                                bigger_uom = residual_qty//closest_value

                                prepared_uom_unit = str(
                                    int(bigger_uom)) + ' x ' + str(package_name)
                                final_uom_unit.append(prepared_uom_unit)

                                smaller_uom = residual_qty % closest_value
                                loop_value = smaller_uom

                                if bigger_uom >= 1 and smaller_uom != 0:
                                    residual_qty = residual_qty % closest_value
                                else:
                                    record.sale_multi_uom_unit = ", ".join(
                                        final_uom_unit)
                                    break

    # check product stock qty
    def check_product_stock_qty(self, product_id, product_uom_qty):
        if product_id and product_uom_qty:
            product_stock_qty = self.env['product.product'].search(
                [('id', '=', product_id.id)]).qty_available
            if product_uom_qty > product_stock_qty:
                raise ValidationError(
                    f"This product is out of stock - {product_id.name}")

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'commission')
    def _compute_amount(self):
        data = super(TAKSaleOrderLine, self)._compute_amount()
        for line in self:
            if line.commission:
                # Calculate commission amount
                commission_rate = line.commission / 100
                commission_value = line.price_subtotal * commission_rate

                # Update commission and subtotal values
                line.update({
                    'commission_amount': commission_value,
                    'price_subtotal': line.price_subtotal - commission_value,
                    'price_total': line.price_total - commission_value,
                })
        return data
