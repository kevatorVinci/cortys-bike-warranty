from psycopg2 import IntegrityError

from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestProductWarranty(TransactionCase):

    def test_warranty_duration_default(self):
        product = self.env["product.template"].create(
            {
                "name": "Product without warranty",
            }
        )

        self.assertEqual(product.warranty_duration_months, 0)

    def test_warranty_duration_positive(self):
        product = self.env["product.template"].create(
            {
                "name": "Bike with warranty",
                "warranty_duration_months": 24,
            }
        )

        self.assertEqual(product.warranty_duration_months, 24)

    def test_warranty_duration_negative(self):
        with mute_logger("odoo.sql_db"):
            with self.assertRaises(IntegrityError):
                with self.cr.savepoint():
                    self.env["product.template"].create(
                        {
                            "name": "Invalid warranty",
                            "warranty_duration_months": -1,
                        }
                    )
                    self.env.flush_all()
