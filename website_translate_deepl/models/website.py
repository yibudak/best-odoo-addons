# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api, fields, _


class Website(models.Model):
    _inherit = "website"

    deepl_account_id = fields.Many2one(
        comodel_name="deepl.account",
        string="DeepL Account",
        required=False,
    )

    def action_translate_contents(self):
        self.ensure_one()
        action = self.env.ref(
            "website_translate_deepl.action_website_translate_wizard"
        ).read()[0]
        action["context"] = {"default_website_id": self.id}
        return action
