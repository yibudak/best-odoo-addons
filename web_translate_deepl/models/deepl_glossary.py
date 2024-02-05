# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import csv
import io
import base64
import requests


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
            # Delete the glossary from DeepL API too.
            for glossary in self.filtered(lambda g: g.deepl_id):
                glossary._api_delete_glossary(glossary.deepl_account_id)

        return super(DeepLGlossary, self).write(vals)

    def unlink(self):
        """
        Delete the glossary from DeepL API before unlinking.
        :return:
        """
        for glossary in self.filtered(lambda g: g.deepl_id):
            glossary._api_delete_glossary(glossary.deepl_account_id)
        return super(DeepLGlossary, self).unlink()

    @api.depends("deepl_id", "source_lang_id", "target_lang_id")
    def _compute_name(self):
        for record in self:
            record.name = f"[{record.deepl_account_id.name}] {record.source_lang_id.name} > {record.target_lang_id.name}"

    def _api_delete_glossary(self, account):
        """
        Delete glossary from DeepL API.
        :param account: deepl.account record
        :return:
        """
        self.ensure_one()
        url = f"https://api.deepl.com/v2/glossaries/{self.deepl_id}"
        headers = {
            "Authorization": f"DeepL-Auth-Key {account.auth_key}",
            "User-Agent": "Odoo/12.0",
        }
        requests.delete(url, headers=headers, timeout=10)
        self.write({"deepl_id": False})

    def _api_create_glossary(self, account):
        """
        Create glossary in DeepL API.
        :param account: deepl.account record
        :return:
        """
        self.ensure_one()
        csv_file = io.StringIO(base64.b64decode(self.entries_csv_file).decode("utf-8"))
        reader = csv.reader(csv_file)
        reader.__next__()  # Skip header
        entries = list(reader)
        entries_text = "\n".join("%s\t%s" % (x[0], x[1]) for x in entries)

        url = "https://api.deepl.com/v2/glossaries"
        headers = {
            "Authorization": f"DeepL-Auth-Key {account.auth_key}",
            "User-Agent": "Odoo/12.0",
        }
        data = {
            "name": self.name,
            "source_lang": self.source_lang_id.code.split("_")[0],
            "target_lang": self.target_lang_id.code.split("_")[0],
            "entries": entries_text,
            "entries_format": "tsv",
        }
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code != 201:
            raise UserError(_("DeepL API Error: %s") % response.text)
        self.write({"deepl_id": response.json().get("glossary_id")})
