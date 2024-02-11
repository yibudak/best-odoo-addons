# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api, fields, _
import logging

_logger = logging.getLogger(__name__)
_SEO_FIELDS = [
    "website_meta_title",
    "website_meta_description",
    "website_meta_keywords",
]


class WebsitePage(models.Model):
    _inherit = "website.page"

    # record.website_meta_title and record.website_meta_description and record.website_meta_keywords
    def remove_seo_translation(self, target_lang_id):
        self.ensure_one()
        for field in _SEO_FIELDS:
            translations = self.get_field_translations(
                field, langs={target_lang_id.code}
            )[0]
            if not translations:
                continue

            updated_fields = {target_lang_id.code: {}}
            for translation in translations:
                if translation["value"]:
                    updated_fields[target_lang_id.code] = translation["source"]
                else:  # Always reset with source language
                    updated_fields[target_lang_id.code] = getattr(self, field)
            if updated_fields[target_lang_id.code]:
                self.update_field_translations(field, updated_fields)
                self.env.cr.commit()
        return True

    def deepl_translate_seo_fields(
        self,
        deepl_account_id,
        source_lang_id,
        target_lang_id,
    ):
        """
        Translate all fields of the view with DeepL API
        :param deepl_account_id: deepl.account
        :param target_lang_id: res.lang
        """
        self.ensure_one()

        for field in _SEO_FIELDS:
            translations = self.get_field_translations(
                field, langs={target_lang_id.code}
            )[0]
            if not translations:
                continue

            updated_fields = {target_lang_id.code: {}}
            for translation in translations:
                if translation["value"]:
                    continue
                try:
                    source_text = translation["source"] or getattr(self, field)

                    # Always try to translate title of the page if it is empty
                    if not source_text and field == "website_meta_title":
                        source_text = self.name

                    if source_text:
                        translated_text = deepl_account_id.translate(
                            text=source_text,
                            source_lang_code=source_lang_id.code,
                            target_lang_code=target_lang_id.code,
                        )
                        updated_fields[target_lang_id.code] = translated_text
                except Exception as e:
                    _logger.error(
                        "Error while translating field '%s' in view %s [%s]: %s",
                        translation["source"],
                        self.name,
                        self.id,
                        e,
                    )
                    continue
            if updated_fields[target_lang_id.code]:
                self.update_field_translations(field, updated_fields)
                self.env.cr.commit()
        return True
