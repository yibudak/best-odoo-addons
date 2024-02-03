# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api, fields, _


class ResLang(models.Model):
    _inherit = "res.lang"

    tr_base_lang_id = fields.Many2one(
        "res.lang",
        string="Base Translate Language",
        help="The language to translate from with DeepL API",
    )
