# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    # billing_address_ids = fields.Many2many(
    #     "res.partner",
    #     compute="_compute_address_ids",
    #     string="Billing Addresses",
    # )

    shipping_address_ids = fields.Many2many(
        "res.partner",
        compute="_compute_address_ids",
        string="Shipping Addresses",
    )

    def _compute_address_ids(self):
        # Todo check and optimize
        for partner in self:
            # partner.billing_address_ids = self.search(
            #     [
            #         '|',
            #         ('id', '=', partner.id),
            #         '&',
            #         ("id", "child_of", partner.commercial_partner_id.ids),
            #         "|",
            #         ("type", "in", ["invoice", "contact"]),
            #         ("id", "=", partner.commercial_partner_id.id),
            #     ],
            #     order="id desc",
            # )
            partner.shipping_address_ids = self.search(
                [
                    ("id", "child_of", partner.commercial_partner_id.ids),
                    "|",
                    ("type", "in", ["delivery", "other"]),
                    ("id", "=", partner.commercial_partner_id.id),
                ],
                order="id desc",
            )
