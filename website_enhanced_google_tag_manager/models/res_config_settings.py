# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    google_tag_manager_key = fields.Char(
        "Container ID",
        related="website_id.google_tag_manager_key",
        readonly=False,
    )
    ecommerce_conversion = fields.Boolean(
        "E-Commerce Conversion",
        related="website_id.ecommerce_conversion",
        readonly=False,
    )
