from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    warranty_duration_months = fields.Integer(
        string="Warranty Duration (Months)",
        default=0,
        help="Warranty duration from the initial customer delivery date. "
        "Set to 0 for no warranty.",
    )

    _warranty_duration_non_negative = models.Constraint(
        "CHECK(warranty_duration_months >= 0)",
        "The warranty duration cannot be negative.",
    )
