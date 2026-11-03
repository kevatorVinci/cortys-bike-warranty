from dateutil.relativedelta import relativedelta

from odoo import Command, fields
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestBikeWarranty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Client garantie"})
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.env.company.id)], limit=1
        )
        cls.bike = cls.env["product.product"].create(
            {
                "name": "Vélo garanti",
                "type": "consu",
                "is_storable": True,
                "tracking": "serial",
                "warranty_duration_months": 24,
            }
        )
        cls.part = cls.env["product.product"].create(
            {
                "name": "Pièce test",
                "type": "consu",
                "is_storable": True,
                "list_price": 50.0,
            }
        )

    def _deliver_bike(self, months_ago=0):
        """Livre un vélo neuf au client et renvoie (lot, move_line)."""
        lot = self.env["stock.lot"].create(
            {
                "name": f"SN-{self.env['stock.lot'].search_count([]) + 1}",
                "product_id": self.bike.id,
                "company_id": self.env.company.id,
            }
        )
        stock_location = self.warehouse.lot_stock_id
        customer_location = self.env.ref("stock.stock_location_customers")
        self.env["stock.quant"]._update_available_quantity(
            self.bike, stock_location, 1.0, lot_id=lot
        )
        picking = self.env["stock.picking"].create(
            {
                "partner_id": self.partner.id,
                "picking_type_id": self.warehouse.out_type_id.id,
                "location_id": stock_location.id,
                "location_dest_id": customer_location.id,
                "move_ids": [
                    Command.create(
                        {
                            "product_id": self.bike.id,
                            "product_uom_qty": 1.0,
                            "location_id": stock_location.id,
                            "location_dest_id": customer_location.id,
                        }
                    )
                ],
            }
        )
        picking.action_confirm()
        picking.action_assign()
        picking.move_line_ids.write({"lot_id": lot.id, "quantity": 1.0})
        picking.button_validate()
        self.assertEqual(picking.state, "done")
        move_line = picking.move_line_ids
        if months_ago:
            move_line.date = fields.Datetime.now() - relativedelta(months=months_ago)
        return lot, move_line

    def _create_repair(self, lot, **extra):
        vals = {
            "product_id": self.bike.id,
            "lot_id": lot.id,
            "partner_id": self.partner.id,
        }
        vals.update(extra)
        return self.env["repair.order"].create(vals)

    def test_recent_delivery_under_warranty(self):
        lot, move_line = self._deliver_bike(months_ago=6)
        repair = self._create_repair(lot)

        self.assertEqual(repair.delivery_date, move_line.date)
        self.assertEqual(
            repair.warranty_end_date,
            move_line.date.date() + relativedelta(months=24),
        )
        self.assertEqual(repair.warranty_status, "covered")
        repair.action_check_warranty()
        self.assertTrue(repair.under_warranty)

    def test_expired_warranty(self):
        lot, move_line = self._deliver_bike(months_ago=30)
        repair = self._create_repair(lot)

        self.assertEqual(
            repair.warranty_end_date,
            move_line.date.date() + relativedelta(months=24),
        )
        self.assertFalse(repair.under_warranty)

    def test_no_delivery_no_warranty(self):
        lot = self.env["stock.lot"].create(
            {
                "name": "SN-NO-DELIVERY",
                "product_id": self.bike.id,
                "company_id": self.env.company.id,
            }
        )
        repair = self._create_repair(lot)

        self.assertFalse(repair.delivery_date)
        self.assertFalse(repair.warranty_end_date)
        self.assertFalse(repair.under_warranty)

    def test_zero_duration_no_warranty(self):
        self.bike.warranty_duration_months = 0
        lot, _move_line = self._deliver_bike(months_ago=1)
        repair = self._create_repair(lot)

        self.assertFalse(repair.warranty_end_date)
        self.assertFalse(repair.under_warranty)

    def test_warranty_parts_and_completion(self):
        lot, _move_line = self._deliver_bike(months_ago=6)
        self.env["stock.quant"]._update_available_quantity(
            self.part, self.warehouse.lot_stock_id, 5.0
        )
        repair = self._create_repair(
            lot,
            move_ids=[
                Command.create(
                    {
                        "product_id": self.part.id,
                        "product_uom_qty": 1.0,
                        "repair_line_type": "add",
                    }
                )
            ],
        )
        self.assertEqual(repair.warranty_status, "covered")
        repair.action_check_warranty()
        self.assertTrue(repair.under_warranty)

        # Pièce non facturée sous garantie
        repair.action_create_sale_order()
        sale_line = repair.sale_order_id.order_line.filtered(
            lambda line: line.product_id == self.part
        )
        self.assertTrue(sale_line)
        self.assertEqual(sale_line.price_unit, 0.0)

        # Terminer la réparation
        end_date_before = repair.warranty_end_date
        delivery_before = repair.delivery_date
        repair.action_repair_start()
        repair.action_repair_end()
        self.assertEqual(repair.state, "done")

        # La garantie n'a pas été prolongée
        self.assertEqual(repair.warranty_end_date, end_date_before)
        self.assertEqual(repair.delivery_date, delivery_before)
