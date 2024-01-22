# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    fcm_device_ids = fields.One2many(
        "fcm.device",
        "partner_id",
        string="FCM Devices",
        help="Firebase Cloud Messaging Devices",
    )
