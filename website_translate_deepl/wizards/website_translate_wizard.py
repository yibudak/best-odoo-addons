# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class WebsiteTranslateWizard(models.TransientModel):
    _name = "website.translate.wizard"
    _description = "Website Translate Wizard"

    website_id = fields.Many2one(
        "website",
        string="Website",
        required=True,
    )
    target_lang_id = fields.Many2one(
        "res.lang",
        string="Target Language",
        domain="[('active', '=', True)]",
        required=True,
    )
    override_translations = fields.Boolean(
        string="Override Translations",
        default=False,
        help="Override existing translations",
    )

    def action_translate_seo(self):
        self.ensure_one()
        self._translate_all_seo()
        return {"type": "ir.actions.act_window_close"}

    def action_translate_content(self):
        self.ensure_one()
        self._translate_all_content()
        return {"type": "ir.actions.act_window_close"}

    def action_translate_menus(self):
        self.ensure_one()
        self._translate_all_menus()
        return {"type": "ir.actions.act_window_close"}

    # website.page functions

    def _get_website_pages(self):
        return self.env["website.page"].search(
            [
                "|",
                ("active", "=", False),
                ("active", "=", True),
                ("is_published", "=", True),
                ("is_seo_optimized", "=", True),
                ("website_id", "=", self.website_id.id),
            ]
        )

    def _translate_all_seo(self):
        pages = self._get_website_pages()
        for page in pages:
            page.with_context(
                lang=self.website_id.default_lang_id.code
            ).with_delay().deepl_translate_seo_fields(
                deepl_account_id=self.website_id.deepl_account_id,
                source_lang_id=self.website_id.default_lang_id,
                target_lang_id=self.target_lang_id,
                translation_override=self.override_translations,
            )

    # ir.ui.view functions

    def _get_website_views(self):
        return self.env["ir.ui.view"].search(
            [
                "|",
                ("active", "=", False),
                ("active", "=", True),
                ("website_id", "=", self.website_id.id),
            ]
        )

    def _translate_all_content(self):
        views = self._get_website_views()
        for view in views:
            view.with_delay().deepl_translate_all_fields(
                deepl_account_id=self.website_id.deepl_account_id,
                source_lang_id=self.website_id.default_lang_id,
                target_lang_id=self.target_lang_id,
                translation_override=self.override_translations,
            )

    # website.menu functions

    def _get_website_menus(self):
        return self.env["website.menu"].search(
            [
                ("website_id", "=", self.website_id.id),
            ]
        )

    def _translate_all_menus(self):
        menus = self._get_website_menus()
        for menu in menus:
            menu.with_delay().deepl_translate_menu(
                deepl_account_id=self.website_id.deepl_account_id,
                source_lang_id=self.website_id.default_lang_id,
                target_lang_id=self.target_lang_id,
                translation_override=self.override_translations,
            )
