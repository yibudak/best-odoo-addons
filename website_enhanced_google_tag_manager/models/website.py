# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class Website(models.Model):
    _inherit = "website"

    google_tag_manager_key = fields.Char("Container ID")
    ecommerce_conversion = fields.Boolean(
        "E-Commerce Conversion", default=False
    )
