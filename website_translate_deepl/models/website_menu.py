# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api, fields, _


class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    def remove_translation(self, target_lang_id):
        """
        Remove the menu translations for the given language
        :param lang_id: res.lang
        """
        self.ensure_one()
        fields
