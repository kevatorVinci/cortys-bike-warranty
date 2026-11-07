from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    customer_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Produits achetés par le client",
        compute="_compute_customer_product_ids",
    )
    customer_lot_ids = fields.Many2many(
        comodel_name="stock.lot",
        string="Numéros de série livrés au client",
        compute="_compute_customer_lot_ids",
    )

    @api.depends("partner_id", "company_id")
    def _compute_customer_product_ids(self):
        SaleLine = self.env["sale.order.line"]
        for order in self:
            products = self.env["product.product"]
            if order.partner_id:
                partner = order.partner_id.commercial_partner_id
                lines = SaleLine.search(
                    [
                        ("order_id.state", "in", ["sale", "done"]),
                        ("order_id.partner_id.commercial_partner_id", "=", partner.id),
                        ("order_id.company_id", "=", order.company_id.id),
                        ("product_id", "!=", False),
                        ("display_type", "=", False),
                    ]
                )
                products = lines.product_id
            order.customer_product_ids = products

    @api.depends("partner_id", "product_id", "company_id")
    def _compute_customer_lot_ids(self):
        MoveLine = self.env["stock.move.line"]
        for order in self:
            lots = self.env["stock.lot"]
            if order.partner_id and order.product_id:
                partner = order.partner_id.commercial_partner_id
                lines = MoveLine.search(
                    [
                        ("state", "=", "done"),
                        ("lot_id", "!=", False),
                        ("product_id", "=", order.product_id.id),
                        ("picking_id.picking_type_id.code", "=", "outgoing"),
                        ("location_dest_id.usage", "=", "customer"),
                        (
                            "picking_id.partner_id.commercial_partner_id",
                            "=",
                            partner.id,
                        ),
                        ("company_id", "=", order.company_id.id),
                    ]
                )
                lots = lines.lot_id
            order.customer_lot_ids = lots

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_clear_selection(self):
        if self.product_id and self.product_id not in self.customer_product_ids:
            self.product_id = False
        if self.lot_id and self.lot_id not in self.customer_lot_ids:
            self.lot_id = False
        self.under_warranty = False

    @api.onchange("product_id")
    def _onchange_product_clear_lot(self):
        if self.lot_id and self.lot_id not in self.customer_lot_ids:
            self.lot_id = False
