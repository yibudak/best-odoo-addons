# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api, fields, _


class ResCompany(models.Model):
    _inherit = "res.company"

    deepl_account_id = fields.Many2one(
        comodel_name="deepl.account",
        string="DeepL Account",
        required=False,
    )

    # base_lang = fields.Many2one(
    #     comodel_name="res.lang",
    #     string="Base Language",
    #     required=False,
    # )
