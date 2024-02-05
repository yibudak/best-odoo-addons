# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models, _


class DeepLGlossary(models.Model):
    _name = "deepl.glossary"
    _description = "DeepL Glossary"

    name = fields.Char(string="Name", compute="_compute_name", store=True)
    deepl_account_id = fields.Many2one(
        "deepl.account",
        string="DeepL Account",
        required=True,
    )
    deepl_id = fields.Char(string="DeepL ID", readonly=True)
    source_lang_id = fields.Many2one(
        "res.lang",
        string="Source Language",
        required=True,
    )
    target_lang_id = fields.Many2one(
        "res.lang",
        string="Target Language",
        required=True,
    )
    entries_csv_file = fields.Binary(string="Entries CSV File")

    @api.model
    def write(self, vals):
        """
        Reset deepl_id to False if any change is made.
        :param vals:
        :return:
        """
        if "deepl_id" not in vals:
            vals["deepl_id"] = False
        return super(DeepLGlossary, self).write(vals)

    @api.depends("deepl_id", "source_lang_id", "target_lang_id")
    def _compute_name(self):
        for record in self:
            record.name = f"[{record.deepl_account_id.name}] {record.source_lang_id.name} > {record.target_lang_id.name}"
