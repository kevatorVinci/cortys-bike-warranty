from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    warranty_status = fields.Selection(
        [
            ("missing", "Informations manquantes"),
            ("none", "Aucune garantie"),
            ("covered", "Sous garantie"),
            ("expired", "Garantie expirée"),
        ],
        string="Warranty Status",
        compute="_compute_warranty_status",
    )
    delivery_date = fields.Datetime(
        string="Customer Delivery Date",
        compute="_compute_delivery_date",
    )
    warranty_end_date = fields.Date(
        string="Warranty End Date",
        compute="_compute_warranty_end_date",
    )

    def _get_warranty_reference_date(self):
        self.ensure_one()
        return (self.schedule_date or fields.Datetime.now()).date()

    def _get_warranty_status(self):
        self.ensure_one()
        if not self.product_id or not self.lot_id or not self.delivery_date:
            return "missing"

        months = self.product_id.product_tmpl_id.warranty_duration_months
        if months <= 0:
            return "none"

        end_date = self.delivery_date.date() + relativedelta(months=months)
        reference = self._get_warranty_reference_date()
        if reference < self.delivery_date.date():
            return "missing"
        return "covered" if reference <= end_date else "expired"

    @api.depends("delivery_date", "schedule_date", "product_id", "lot_id")
    def _compute_warranty_status(self):
        for order in self:
            order.warranty_status = order._get_warranty_status()

    def action_check_warranty(self):
        for order in self:
            order.write({"under_warranty": order._get_warranty_status() == "covered"})
        return True

    @api.depends("lot_id", "product_id", "partner_id", "company_id")
    def _compute_delivery_date(self):
        for order in self:
            order.delivery_date = False
            if not order.lot_id or not order.product_id:
                continue
            domain = [
                ("lot_id", "=", order.lot_id.id),
                ("product_id", "=", order.product_id.id),
                ("company_id", "=", order.company_id.id),
                ("state", "=", "done"),
                ("picking_code", "=", "outgoing"),
                ("location_dest_usage", "=", "customer"),
            ]
            if order.partner_id:
                domain.append(("picking_partner_id", "=", order.partner_id.id))
            line = self.env["stock.move.line"].search(
                domain,
                order="date asc",
                limit=1,
            )
            order.delivery_date = line.date

    @api.depends(
        "delivery_date",
        "product_id",
        "product_id.product_tmpl_id.warranty_duration_months",
    )
    def _compute_warranty_end_date(self):
        for order in self:
            months = (
                order.product_id.product_tmpl_id.warranty_duration_months
                if order.product_id
                else 0
            )
            if order.delivery_date and months > 0:
                order.warranty_end_date = order.delivery_date.date() + relativedelta(
                    months=months
                )
            else:
                order.warranty_end_date = False
